from main import CONFERENCE_ROOM_TOTAL_SEATS
import cpmpy as cp

start_time = cp.intvar(lb=0, ub=24)
end_time = cp.intvar(lb=0, ub=24)
required_seats = 5



cp.constrain(required_seats <= CONFERENCE_ROOM_TOTAL_SEATS)

cp.no_overlap([start_time, end_time] for start_time, end_time in meetings)

model = Model()

model.add_constraints(start_time, end_time)
solver = CPlex(model)
solver.solve()

