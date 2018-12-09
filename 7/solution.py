import re
import collections
import datetime


pattern = re.compile(r"Step (?P<step>\w) must be finished before step (?P<next_step>\w) can begin.")


class Step(object):

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, _id):
        self.id = _id
        self.time_elapsed = 0
        self.time_to_complete = self.alphabet.index(self.id) + 61
        self.next_steps = []
        self.prev_steps = []
        self.has_completed = False

    def __hash__(self):
        return self.id

    def __eq__(self, _step):
        return self.id == _step.id

    def __repr__(self):
        # return "%s: %s" % (self.id, self.next_steps)
        return "%s: %s/%s" % (self.id, self.time_elapsed, self.time_to_complete)

    def can_run(self):
        return not self.has_completed and \
            (len(self.prev_steps) == 0 or all([prev.has_completed for prev in self.prev_steps]))


    

def read_input(filename):
    steps = {}
    with open(filename) as f:
        for line in [l.replace('\n', '') for l in f.readlines()]:
            match = pattern.match(line)
            if match:
                step_id = match.group('step')
                if step_id not in steps.keys():
                    steps[step_id] = Step(step_id)
                next_step_id = match.group('next_step')
                if next_step_id not in steps.keys():
                    steps[next_step_id] = Step(next_step_id)
                step = steps[step_id]
                next_step = steps[next_step_id]
                step.next_steps.append(next_step)
                next_step.prev_steps.append(step)
    # print [s.id for s in sorted(steps.values(), key=lambda s: s.id)]
    return sorted(steps.values(), key=lambda s: s.id)


def get_next(sorted_steps):
    # print [s.id for s in sorted_steps]
    for step in sorted_steps:
        if step.can_run():
            return step

def part1(steps):
    steps_remaining = steps
    steps_run = []
    while len(steps_remaining) > 0:
        next_step = get_next(steps_remaining)
        next_step.has_completed = True
        steps_run.append(next_step)
        steps_remaining = [s for s in steps_remaining if not s.has_completed]
    
    print ''.join([s.id for s in steps_run])


def get_next_list(sorted_steps, num_idle_workers):
    return [step for step in sorted_steps if step.can_run()][:num_idle_workers]


def part2(steps, max_running_tasks):
    queued_steps = steps
    running_steps = []
    time = 0
    while len(queued_steps) > 0 or len(running_steps) > 0:
        next_steps = get_next_list(queued_steps, max_running_tasks - len(running_steps))
        running_steps = running_steps + next_steps
        print "%s\t%s\t%s" % (time, running_steps, queued_steps)

        time += 1
        for s in running_steps:
            s.time_elapsed += 1

        queued_steps = [s for s in queued_steps if s.time_elapsed == 0]
        completed_steps = [s for s in running_steps if s.time_elapsed == s.time_to_complete]
        running_steps = [s for s in running_steps if s.time_elapsed < s.time_to_complete]
        for s in completed_steps:
            s.has_completed = True
    return time
    

        

