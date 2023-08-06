import sys

import dpsim
import _dpsim

def multiply_decoupled(sys, num_copies, nodes, resistance, inductance, capacitance):
    sys.multiply(num_copies)
    counter = 0
    for orig_node in nodes:
        node_names = [orig_node]
        node_names += [orig_node + '_' + str(i) for i in range(2, num_copies+2)]
        node_names.append(orig_node)
        for i in range(0, num_copies+1):
            sys.add_decoupling_line('dline' + str(counter), sys.nodes[node_names[i]], sys.nodes[node_names[i+1]], resistance, inductance, capacitance)
            counter += 1

def multiply_coupled(sys, num_copies, nodes, resistance, inductance, capacitance):
    gnd = dpsim.dp.Node.GND()
    sys.multiply(num_copies)
    counter = 0
    for orig_node in nodes:
        node_names = [orig_node]
        node_names += [orig_node + '_' + str(i) for i in range(2, num_copies+2)]
        node_names.append(orig_node)
        for i in range(0, num_copies+1):
            # TODO lumped resistance?
            rl_node = dpsim.dp.Node('N_add_' + str(counter))
            res = dpsim.dp.ph1.Resistor('R_' + str(counter))
            res.R = resistance
            ind = dpsim.dp.ph1.Inductor('L_' + str(counter))
            ind.L = inductance
            cap1 = dpsim.dp.ph1.Capacitor('C1_' + str(counter))
            cap1.C = capacitance / 2
            cap2 = dpsim.dp.ph1.Capacitor('C2_' + str(counter))
            cap2.C = capacitance / 2

            sys.add_node(rl_node)
            res.connect([sys.nodes[node_names[i]], rl_node])
            ind.connect([rl_node, sys.nodes[node_names[i+1]]])
            cap1.connect([sys.nodes[node_names[i]], gnd])
            cap2.connect([sys.nodes[node_names[i+1]], gnd])
            counter += 1

            sys.add_component(res)
            sys.add_component(ind)
            sys.add_component(cap1)
            sys.add_component(cap2)

def multiply_diakoptics(sys, num_copies, nodes, resistance, inductance, capacitance, splits=0):
    gnd = dpsim.dp.Node.GND()
    sys.multiply(num_copies)
    counter = 0
    tear_components = []
    if splits > 0:
        split_every = int(num_copies+1) / splits
    else:
        split_every = 1
    for orig_node in nodes:
        node_names = [orig_node]
        node_names += [orig_node + '_' + str(i) for i in range(2, num_copies+2)]
        node_names.append(orig_node)
        for i in range(0, num_copies+1):
            line = dpsim.dp.ph1.PiLine('line' + str(counter))
            line.R_series = resistance
            line.L_series = inductance
            line.C_parallel = capacitance
            line.connect([sys.nodes[node_names[i]], sys.nodes[node_names[i+1]]])
            if i % split_every == 0:
                tear_components.append(line)
            else:
                sys.add_component(line)
            counter += 1
    return tear_components


def map_scheduler(sched_string, size=0):
    parts = sched_string.split(' ')
    scheduler = parts[0]
    sched_args = {}
    for s in parts:
        if s.isdigit():
            sched_args['threads'] = int(s)
        elif s == 'meas':
            if size:
                sched_args['in_measurement_file'] = 'measurements_'+str(size)+'.txt'
            else:
                sched_args['in_measurement_file'] = 'measurements.txt'
        elif s == 'cv':
            sched_args['use_condition_variable'] = True
        elif s == 'tasktype':
            sched_args['sort_task_types'] = True
    return (scheduler, sched_args)

def do_meas(instance, size=0):
    instance = copy.copy(instance)
    instance.repetitions = 1
    if size:
        filename = 'measurements_'+str(size)+'.txt'
    else:
        filename = 'measurements.txt'
    instance.do_sim(scheduler='sequential', scheduler_args={'out_measurement_file': filename}, size=size)

def check_numa():
    try:
        import numa
    except:
        return
    if not numa.available():
        return
    if numa.get_max_node() > 0 and len(numa.get_run_on_node_mask()) > 1:
        print("Warning: NUMA settings may be suboptimal!", file=sys.stderr)

class SimInstance:
    """ Helper class that embeds all parameters that stay constant for multiple
        runs of a simulation, e.g. for a performance plot.
    """

    def __init__(self, name, files, frequency, repetitions=1):
        self.name = name
        self.files = files
        self.frequency = frequency
        self.repetitions = repetitions
        try:
            self.version = _dpsim.__version__
        except:
            self.version = 'unknown'
        self.hostname = socket.gethostname()
        self.sim_args = {}
        self.copy_settings = None

    def do_sim(self, scheduler=None, scheduler_args={}, size=1):
        times = []
        if size > 1:
            # TODO a bit ugly
            copy_args = self.copy_settings.copy()
            decouple = copy_args['decouple']
            del(copy_args['decouple'])
        for i in range(0, self.repetitions):
            sys = dpsim.load_cim(self.name, self.files, self.frequency, log_level=0)
            if size > 1:
                if decouple == 'diakoptics':
                    self.sim_args['tear_components'] = multiply_diakoptics(sys, size-1, **copy_args)
                elif decouple:
                    multiply_decoupled(sys, size-1, **copy_args)
                else:
                    multiply_coupled(sys, size-1, **copy_args)
            sim = dpsim.Simulation(self.name, sys, **self.sim_args)
            if scheduler:
                sim.set_scheduler(scheduler, **scheduler_args)
            sim.run()
            times.append(sim.avg_step_time)
            if 'tear_components' in self.sim_args:
               del(self.sim_args['tear_components'])
        avg = sum(times)/len(times)
        sigma = math.sqrt(sum([(x - avg)**2 for x in times]) / len(times))
        return (avg, sigma)
