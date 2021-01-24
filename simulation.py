import numpy as np


class Simulation:
    def __init__(
            self,
            *,
            number_of_workers: int,
            queue_length: int,
            avg_arrivals_per_minute: float,
            avg_worker_throughput_per_minute: float
    ):
        self.number_of_workers = number_of_workers
        self.queue_length = queue_length
        self.avg_arrivals_per_minute = avg_arrivals_per_minute
        self.avg_worker_throughput_per_minute = avg_worker_throughput_per_minute

        self.people_in_system = 0

        self.clock = 0
        self.next_arrival_time = self.generate_next_arrival_time()
        self.departure_times = [float('inf')] * self.number_of_workers

        self.total_arrivals = 0
        self.total_departures = 0
        self.people_serviced_immediately = 0
        self.people_denied = 0
        self.total_time_in_system = 0.0
        self.total_wait_time = 0.0

    @property
    def people_accepted(self) -> int:
        return self.total_arrivals - self.people_denied

    @property
    def avg_time_in_system(self) -> float:
        return (
            self.total_time_in_system / (self.total_arrivals - self.people_denied)
            if self.total_arrivals > 0
            else 0.0
        )

    @property
    def avg_wait_time(self) -> float:
        return (
            self.total_wait_time / (self.total_arrivals - self.people_denied)
            if self.total_arrivals > 0
            else 0.0
        )

    @property
    def avg_service_time(self) -> float:
        return self.avg_time_in_system - self.avg_wait_time

    @property
    def no_wait_probability(self) -> float:
        return (
            self.people_serviced_immediately / self.total_arrivals
            if self.total_arrivals > 0
            else 0.0
        )

    @property
    def acceptance_probability(self) -> float:
        return (
            self.people_accepted / self.total_arrivals
            if self.total_arrivals > 0
            else 0.0
        )

    @property
    def denial_probability(self) -> float:
        return (
            self.people_denied / self.total_arrivals
            if self.total_arrivals > 0
            else 0.0
        )

    @property
    def immediate_service_probability(self) -> float:
        return (
            self.people_serviced_immediately / self.total_arrivals
            if self.total_arrivals > 0
            else 0.0
        )

    def advance_time(self) -> None:
        next_departure_time = min(self.departure_times)
        next_event_time = min(self.next_arrival_time, next_departure_time)
        time_increment = next_event_time - self.clock

        self.total_time_in_system += self.people_in_system * time_increment

        if self.people_in_system > self.number_of_workers:
            self.total_wait_time += (self.people_in_system - self.number_of_workers) * time_increment

        self.clock = next_event_time

        if self.next_arrival_time <= next_departure_time:
            self.handle_arrival()
        else:
            self.handle_departure(worker_index=self.departure_times.index(next_departure_time))

    def handle_arrival(self) -> None:
        self.total_arrivals += 1
        print(f'[{self.clock:.2f} minutes] A person #{self.total_arrivals} has arrived. ', end='')

        if self.people_in_system < (self.number_of_workers + self.queue_length):
            self.people_in_system += 1

            if self.people_in_system <= self.number_of_workers:
                self.people_serviced_immediately += 1
                free_worker_index = self.departure_times.index(float('inf'))
                self.departure_times[free_worker_index] = self.clock + self.generate_service_duration()
                print(f'The will be serviced immediately by worker #{free_worker_index + 1}. ', end='')
            else:
                print(f'The will be put into the queue. ', end='')
        else:
            self.people_denied += 1
            print(f'They will be denied of service (the system is full). ', end='')

        self.next_arrival_time = self.generate_next_arrival_time()
        print(f'Next arrival is scheduled for {self.next_arrival_time:.2f} minutes')

    def handle_departure(self, worker_index: int) -> None:
        queue_not_empty = self.people_in_system > self.number_of_workers

        self.people_in_system -= 1
        self.total_departures += 1
        print(f'[{self.clock:.2f} minutes] A person has just departed from worker #{worker_index + 1}. ', end='')

        if queue_not_empty:
            self.departure_times[worker_index] = self.clock + self.generate_service_duration()
            print('Next person from the queue is invited to the worker')
        else:
            self.departure_times[worker_index] = float('inf')
            print('The worker is now idle')

    def generate_next_arrival_time(self) -> float:
        return self.clock + np.random.exponential(1 / self.avg_arrivals_per_minute)

    def generate_service_duration(self) -> float:
        return np.random.exponential(1 / self.avg_worker_throughput_per_minute)
