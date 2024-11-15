#!/usr/bin/python3
import numpy as np

# คำถามข้อที่ 1: ฟังก์ชันสำหรับประเมินค่าเส้นทางการเคลื่อนที่ของหุ่นยนต์โดยใช้ Quintic Polynomial
def polyTrajEval(t, C, t_i):
    """
    Evaluate the polynomial trajectory at a given time.

    :param t: float, the time at which to evaluate the trajectory
        เวลาปัจจุบันของการเคลื่อนที่ (t ∈ R)
    :param C: np.ndarray, coefficients of the polynomials (num_dof, num_intervals, 6)
        coefficients ของสมการ Quintic Polynomial (C ∈ R^N×M×K)
        - N: จำนวนมิติของการเคลื่อนที่
        - M: จำนวน sub trajectory
        - 6: จำนวน coefficients ของสมการ Quintic Polynomial
    :param t_i: list, time intervals
        เวลาเริ่มต้นของแต่ละ sub trajectory (t_i ∈ R^K)
    :return: tuple of lists (p, v, a) for position, velocity, and acceleration
        - p: ตำแหน่ง ที่ เวลา t (p ∈ R^N)
        - v: ความเร็ว ที่ เวลา t (v ∈ R^N)
        - a: ความเร่ง ที่ เวลา t (a ∈ R^N)
    """
    try:
        # ตรวจสอบว่า t อยู่ในช่วงเวลาที่กำหนด
        if t >= t_i[-1]:
            interval_index = len(t_i) - 2  # เลือก sub trajectory สุดท้ายถ้า t อยู่เกินช่วงเวลาที่กำหนด
        else:
            interval_index = np.searchsorted(t_i, t, side='right') - 1  # หาช่วงเวลา (sub trajectory) ที่ t อยู่ในนั้น
            if interval_index < 0 or interval_index >= len(t_i) - 1:
                raise ValueError("Time t is out of bounds of the provided time intervals.")

        t_offset = t - t_i[interval_index]  # หาค่า offset ของ t ภายใน sub trajectory ที่เลือก
        coefficients = C[:, interval_index, :]  # ดึง coefficients ของ sub trajectory ที่เลือกออกมา

        # เติม coefficients ถ้าน้อยกว่า 6
        if coefficients.shape[1] < 6:
            padded_coefficients = np.zeros((coefficients.shape[0], 6))
            padded_coefficients[:, -coefficients.shape[1]:] = coefficients
            coefficients = padded_coefficients

        # คำนวณตำแหน่ง (p), ความเร็ว (v), และความเร่ง (a) ที่ เวลา t
        p = [np.polyval(c, t_offset) for c in coefficients]  # ประเมินค่าตำแหน่ง
        v = [np.polyval(np.polyder(c), t_offset) for c in coefficients]  # ประเมินค่าความเร็ว (โดยการหา diff ครั้งที่ 1)
        a = [np.polyval(np.polyder(c, 2), t_offset) for c in coefficients]  # ประเมินค่าความเร่ง (โดยการหา diff ครั้งที่ 2)

        return p, v, a

    except Exception as e:
        print(f"Error in polyTrajEval: {e}")
        return None, None, None

# คำถามข้อที่ 2: ฟังก์ชันสำหรับสร้าง coefficients ของสมการ Quintic Polynomial ในรูปแบบของ Configuration Space
def HW4TrajGen(via_points):
    """
    Generate trajectory coefficients for a given set of via points.

    :param via_points: np.ndarray or list, shape (num_dof, num_points)
        จุด via points ที่หุ่นยนต์จะต้องเคลื่อนที่ผ่าน (via_points ∈ R^3×(K+1))
        - 3: จำนวนแกน (XYZ)
        - (K+1): จำนวนจุดที่หุ่นยนต์ต้องเคลื่อนที่ผ่าน
    :return: tuple (C, t_i, T, flag)
        - C: coefficients ของสมการ Quintic Polynomial (C ∈ R^N×M×K)
        - t_i: เวลาเริ่มต้นของแต่ละ sub trajectory (t_i ∈ R^K)
        - T: เวลารวมทั้งหมดที่ใช้ในการเคลื่อนที่
        - flag: ตัวบอกสถานะการสร้างคำสั่ง (flag ∈ {0, 1})
            - 1: สามารถสร้างคำสั่งการเคลื่อนที่ได้
            - 0: มี Error ในการสร้างคำสั่งการเคลื่อนที่
    """
    try:
        via_points = np.array(via_points)  # แปลง via points เป็น numpy array
        num_dof, num_points = via_points.shape
        num_intervals = num_points - 1  # จำนวน sub trajectory
        total_time = 120.0  # เวลารวมทั้งหมด (ต้องไม่เกิน 120 s ตามที่โจทย์กำหนด)
        t_i = np.linspace(0, total_time, num_intervals + 1).tolist()  # สร้าง list ของเวลาเริ่มต้นแต่ละ sub trajectory

        # กำหนด coefficients ของสมการ Quintic Polynomial ให้มีจำนวน 6 ตัวในแต่ละ sub trajectory
        C = np.zeros((num_dof, num_intervals, 6))
        flag = 1  # ตีว่าไม่มี Error ในการ Init

        for i in range(num_dof):  # สำหรับแต่ละมิติของการเคลื่อนที่
            for j in range(num_intervals):  # สำหรับแต่ละ sub trajectory
                p0, pf = via_points[i, j], via_points[i, j + 1]  # ตำแหน่งเริ่มต้น และตำแหน่งปลายทาง
                v0, vf = 0, 0  # ความเร็วเริ่มต้น และความเร็วปลายทางเป็นศูนย์
                a0, af = 0, 0  # ความเร่งเริ่มต้น และความเร่งปลายทางเป็นศูนย์
                delta_T = t_i[j + 1] - t_i[j]  # ระยะเวลาใน sub trajectory นี้

                # ตรวจสอบ Limit ความเร็ว และความเร่งตามที่กำหนดในโจทย์
                if abs(pf - p0) / delta_T > 1.75 or 2 * abs(pf - p0) / (delta_T**2) > 0.5:
                    flag = 0  # หากมีค่าใดเกิน Limit ให้เปลี่ยน flag เป็น 0
                    raise ValueError(f"Velocity or acceleration exceeds limits! (DOF={i}, Interval={j})")

                # สร้างเมทริกซ์ A และเวกเตอร์ B สำหรับหาค่า coefficients ของสมการ Quintic Polynomial
                A = np.array([
                    [0, 0, 0, 0, 0, 1],
                    [delta_T**5, delta_T**4, delta_T**3, delta_T**2, delta_T, 1],
                    [0, 0, 0, 0, 1, 0],
                    [5 * delta_T**4, 4 * delta_T**3, 3 * delta_T**2, 2 * delta_T, 1, 0],
                    [0, 0, 0, 2, 0, 0],
                    [20 * delta_T**3, 12 * delta_T**2, 6 * delta_T, 2, 0, 0]
                ])
                B = np.array([p0, pf, v0, vf, a0, af])

                # หาค่า coefficients ของสมการ Quintic Polynomial
                C[i, j, :] = np.linalg.solve(A, B)

        return C, t_i, float(total_time), flag

    except Exception as e:
        print(f"Error in HW4TrajGen: {e}")
        return None, None, None, 1
