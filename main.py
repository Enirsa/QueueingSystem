from simulation import Simulation


if __name__ == '__main__':
    s = Simulation(
        number_of_workers=3,
        queue_length=4,
        avg_arrivals_per_minute=12,
        avg_worker_throughput_per_minute=5,
    )

    for _ in range(5000):
        s.advance_time()

    print(
        f'\nSimulation finished. Results:\n'
        f' - arrivals: {s.total_arrivals}\n'
        f' - accepted: {s.people_accepted} ({(s.acceptance_probability * 100):.2f}%)\n'
        f' - denied: {s.people_denied} ({(s.denial_probability * 100):.2f}%)\n'
        f' - average time in system: {s.avg_time_in_system:.2f} minutes\n'
        f' - average waiting time : {s.avg_wait_time:.2f} minutes\n'
        f' - average service time : {s.avg_service_time:.2f} minutes\n'
        f' - people serviced immediately: {s.people_serviced_immediately} ({(s.immediate_service_probability * 100):.2f}%)\n'
    )
