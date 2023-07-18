
velocity = float(input("Enter initial velocity: "))
coefficient = float(input("Enter the coefficient of friction between the car's tires and the road surface: "))


braking_distance = float(velocity**2 / (2*coefficient*9.8))

print("The calculated braking distance is approximately", braking_distance,"meters.")