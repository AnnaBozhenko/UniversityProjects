import pickle
PARKING_MAP = "parking_plan_fitted.jpg"

if __name__ == '__main__':
    with open('parking.dat', 'rb') as f:
        parking = pickle.load(f)

## session 0

    # occupy unreachable area
    # for slot in [x for x in parking.parking_slots if x.path is None or x.occupied]:
    #     slot.occupy()

## session 1

    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0.5, close_to_vehicle_exit = 0, close_to_p_exit = 0.5)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")

## session 2
    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0.5, close_to_vehicle_exit = 0.5, close_to_p_exit = 0)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")

## session 3
    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0, close_to_vehicle_exit = 0.5, close_to_p_exit = 0.5)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")

## session 4
    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 1, close_to_vehicle_exit = 0, close_to_p_exit = 0)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")

## session 5
    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0, close_to_vehicle_exit = 1, close_to_p_exit = 0)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")

## session 6
    # slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0, close_to_vehicle_exit = 0, close_to_p_exit = 1)
    # print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    # parking.generate_navigation_to_slot(slot_and_cost[0])
    # slot_and_cost[0].occupy()

    # parking.save("parking.dat")
    
## session 7
    slot_and_cost = parking.find_optimal_slot(close_to_entrance = 0.4, close_to_vehicle_exit = 0.3, close_to_p_exit = 0.3)
    print(f"Cost to get to slot {slot_and_cost[0].id}: {slot_and_cost[1]}")
    parking.generate_navigation_to_slot(slot_and_cost[0])
    slot_and_cost[0].occupy()

    parking.save("parking.dat")




