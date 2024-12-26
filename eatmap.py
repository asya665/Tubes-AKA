import heapq
import math
import time
import matplotlib.pyplot as plt

class Place:
    def __init__(self, name, rating, latitude, longitude):
        self.name = name
        self.rating = rating
        self.latitude = latitude
        self.longitude = longitude

    def distance_from(self, user_lat, user_lon):
        # Haversine formula to calculate distance between two coordinates (in km)
        radius = 6371  # Earth's radius in km
        lat1, lon1, lat2, lon2 = map(math.radians, [user_lat, user_lon, self.latitude, self.longitude])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

    def __lt__(self, other):
        # Compare places based on rating, breaking ties with distance
        return self.rating > other.rating

def find_best_places_iterative(user_lat, user_lon, places, top_n=5):
    heap = []

    for place in places:
        distance = place.distance_from(user_lat, user_lon)
        heapq.heappush(heap, (-place.rating, distance, place))

    top_places = []
    for _ in range(min(top_n, len(heap))):
        _, _, place = heapq.heappop(heap)
        top_places.append(place)

    return top_places

def find_best_places_recursive(user_lat, user_lon, places, index=0, heap=None, top_n=5):
    if heap is None:
        heap = []

    if index >= len(places):
        top_places = []
        for _ in range(min(top_n, len(heap))):
            _, _, place = heapq.heappop(heap)
            top_places.append(place)
        return top_places

    place = places[index]
    distance = place.distance_from(user_lat, user_lon)
    heapq.heappush(heap, (-place.rating, distance, place))

    return find_best_places_recursive(user_lat, user_lon, places, index + 1, heap, top_n)

def measure_time_and_run(method, user_lat, user_lon, places, repetitions=10):
    times = []

    for _ in range(repetitions):
        start_time = time.perf_counter()  # Start measuring time with higher precision

        if method == "iterative":
            find_best_places_iterative(user_lat, user_lon, places)
        elif method == "recursive":
            find_best_places_recursive(user_lat, user_lon, places)
        else:
            return 0

        end_time = time.perf_counter()  # End measuring time
        elapsed_time = end_time - start_time
        times.append(elapsed_time)

    # Return the average time to reduce fluctuation
    return sum(times) / len(times)

def main():
    # User location
    user_lat = -6.200000
    user_lon = 106.816666

    # List of places (name, rating, latitude, longitude)
    places = [
        Place("Restaurant A", 4.5, -6.201, 106.816),
        Place("Restaurant B", 4.7, -6.202, 106.817),
        Place("Restaurant C", 4.6, -6.203, 106.818),
        Place("Restaurant D", 4.2, -6.204, 106.819),
        Place("Restaurant E", 4.8, -6.205, 106.820),
    ]

    # Sort places by rating to ensure that they are in a predictable order
    places.sort(reverse=True)  # Highest rating first

    # Number of trials
    trials = 10
    repetitions = 10  # Increased repetitions for more stable results
    iterative_times = []
    recursive_times = []

    # Run warm-up to mitigate cold start issues
    measure_time_and_run("iterative", user_lat, user_lon, places, repetitions)
    measure_time_and_run("recursive", user_lat, user_lon, places, repetitions)

    for trial in range(trials):
        iterative_time = measure_time_and_run("iterative", user_lat, user_lon, places, repetitions)
        recursive_time = measure_time_and_run("recursive", user_lat, user_lon, places, repetitions)

        iterative_times.append(iterative_time)
        recursive_times.append(recursive_time)

    # Print average results for last trial
    print("Iterative approach (last trial):")
    for place in find_best_places_iterative(user_lat, user_lon, places):
        distance = place.distance_from(user_lat, user_lon)
        print(f"{place.name} (Rating: {place.rating}, Distance: {distance:.2f} km)")

    print(f"\nAverage running time (iterative): {iterative_times[-1]:.6f} seconds")

    print("\nRecursive approach (last trial):")
    for place in find_best_places_recursive(user_lat, user_lon, places):
        distance = place.distance_from(user_lat, user_lon)
        print(f"{place.name} (Rating: {place.rating}, Distance: {distance:.2f} km)")

    print(f"\nAverage running time (recursive): {recursive_times[-1]:.6f} seconds")

    # Plotting the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, trials + 1), iterative_times, label='Iterative', color='blue', marker='o')
    plt.plot(range(1, trials + 1), recursive_times, label='Recursive', color='green', marker='s')
    plt.xlabel('Trial')
    plt.ylabel('Average Time (seconds)')
    plt.title('Average Execution Time per Trial')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # This ensures the layout is tight and does not cut off any part of the graph
    plt.show()

if __name__ == "__main__":
    main()
