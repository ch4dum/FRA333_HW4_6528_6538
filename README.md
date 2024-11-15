# Homework Assignment 4: Trajectory Generator
# **Quintic Polynomial Trajectory Generation**

This repository implements a **trajectory generation system** for multi-DOF robotic arms using **Quintic Polynomial** equations. It provides smooth motion generation between waypoints, adhering to constraints such as maximum velocity and acceleration.

---

## **Features**

- **Smooth Trajectories**: Uses Quintic Polynomials for position, velocity, and acceleration calculations.
- **Constraint Adherence**:
  - Maximum velocity: $v_{\text{max}} $
  - Maximum acceleration: $ a_{\text{max}} $
  - Total time: $ t_{\text{max}} $
- **Dynamic Time Adjustment**: Ensures that motion satisfies constraints by adjusting time for each segment.

---

## **Mathematical Foundations**

### **1. Quintic Polynomial Equation**
A **Quintic Polynomial** is defined as:
$$
p(t) = c_5 t^5 + c_4 t^4 + c_3 t^3 + c_2 t^2 + c_1 t + c_0
$$

Where:
- $ p(t)$: Position at time $ t $
- $c_0, c_1, \dots, c_5 $ : Coefficients of the polynomial

### **2. Derivatives**
- **Velocity**:
$$
v(t) = \frac{d p(t)}{dt} = 5c_5 t^4 + 4c_4 t^3 + 3c_3 t^2 + 2c_2 t + c_1
$$
- **Acceleration**:
$$
a(t) = \frac{d^2 p(t)}{dt^2} = 20c_5 t^3 + 12c_4 t^2 + 6c_3 t + 2c_2
$$

### **3. System of Equations for Coefficients**
The coefficients of the polynomial are calculated using boundary conditions:
$$
A \cdot C = B
$$
Where:
$$
A = 
\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 1 \\
\Delta T^5 & \Delta T^4 & \Delta T^3 & \Delta T^2 & \Delta T & 1 \\
0 & 0 & 0 & 0 & 1 & 0 \\
5\Delta T^4 & 4\Delta T^3 & 3\Delta T^2 & 2\Delta T & 1 & 0 \\
0 & 0 & 0 & 2 & 0 & 0 \\
20\Delta T^3 & 12\Delta T^2 & 6\Delta T & 2 & 0 & 0
\end{bmatrix}
$$
$$
B = 
\begin{bmatrix}
p_0 \\ p_f \\ v_0 \\ v_f \\ a_0 \\ a_f
\end{bmatrix}
$$

---

## **Functions**

### **1. `polyTrajEval(t, C, t_i)`**

#### **Purpose**:
Evaluates position, velocity, and acceleration at a given time $ t $.

#### **Input**:
- $ t $ : Time at which the trajectory is evaluated
- $ C $ : Coefficients of the polynomial ($ N \times K \times 6 $)
- $ t_i $ : Starting times of sub-trajectories ($ K $)

#### **Output**:
- Position ($ p $), velocity ($ v $), and acceleration ($ a $) as vectors of size $ N $.

#### **Equations**:
- **Position**:
$$
p(t) = c_5 t^5 + c_4 t^4 + c_3 t^3 + c_2 t^2 + c_1 t + c_0
$$
- **Velocity**:
$$
v(t) = 5c_5 t^4 + 4c_4 t^3 + 3c_3 t^2 + 2c_2 t + c_1
$$
- **Acceleration**:
$$
a(t) = 20c_5 t^3 + 12c_4 t^2 + 6c_3 t + 2c_2
$$

---

### **2. `HW4TrajGen(via_points)`**

#### **Purpose**:
Generates coefficients for a trajectory passing through waypoints.

#### **Input**:
-  via_points : Waypoints ($ N \times K+1 $) where $ N $ is the number of DOFs.

#### **Output**:
- $ C $: Coefficients of the polynomial ($ N \times K \times 6 $)
- $ t_i $: Start times for each segment
- $ T $: Total trajectory time
- $ \text{flag} $ : Success or failure indicator

#### **Process**:
1. **Divide Time into Segments**:
   - Compute time for each segment dynamically to meet constraints:
     - Maximum velocity ($ v_{\text{max}} $).
     - Maximum acceleration ($ a_{\text{max}} $).

2. **Solve for Coefficients**:
   - Using the boundary conditions, solve:
     \[
     A \cdot C = B
     \]

3. **Adjust Time Dynamically**:
   - Increase segment time $ \Delta T $ if constraints are violated.

4. **Output Coefficients**:
   - Polynomial coefficients for each DOF and segment.

---

## **Example Usage**

```python
via_points = np.array([
    [0, 1, 2],  # Waypoints for DOF 1
    [0, -1, 1]  # Waypoints for DOF 2
])

# Generate Trajectory
C, t_i, T, flag = HW4TrajGen(via_points)

if flag:
    # Evaluate the trajectory at t = 1.5 seconds
    t = 1.5
    p, v, a = polyTrajEval(t, C, t_i)
    print("Position:", p)
    print("Velocity:", v)
    print("Acceleration:", a)
else:
    print("Trajectory generation failed.")
```

---

## **Visualization**

To visualize the trajectory, plot position, velocity, and acceleration over time:

```python
import matplotlib.pyplot as plt

# Generate time points
time_points = np.linspace(0, T, 100)
positions, velocities, accelerations = [], [], []

for t in time_points:
    p, v, a = polyTrajEval(t, C, t_i)
    positions.append(p)
    velocities.append(v)
    accelerations.append(a)

# Plot
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time_points, positions)
plt.title("Position vs Time")

plt.subplot(3, 1, 2)
plt.plot(time_points, velocities)
plt.title("Velocity vs Time")

plt.subplot(3, 1, 3)
plt.plot(time_points, accelerations)
plt.title("Acceleration vs Time")

plt.tight_layout()
plt.show()
```

---
