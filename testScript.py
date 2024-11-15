#!/usr/bin/python3
import json
import os
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def import_file():
    for file in os.listdir(os.getcwd()):
        if "fra333" in file:
            print("source code file: " + file)
            exec("from {} import HW4TrajGen, polyTrajEval".format(file[:-3]), globals())
            
def load_json():
    data_json = {}
    with open('testCase.json','r') as f:
        data_json = json.load(f)
    return data_json

def scoreCalculate(data):
    import_file()
    total_score = 0
    for k in range(1,6):
        C_ = np.array(data["q%d" %k]["C"])
        via_point = data["q%d" %k]["via_points"]
        flag_ = data["q%d" %k]["flag"]
        T_ = data["q%d" %k]["T"]
        t_i_ = data["q%d" %k]["t_i"]
        
        try:
                C, t_i, T, flag = HW4TrajGen(via_point)
                if flag != flag_:
                    print("flag doesn't match drop all")
                    return 0
                C = np.array(C)
                
                score_question = 0

                p_ = []
                v_ = []
                a_ = []
                t__ = [i/100 for i in range(int(T*100))]

                # check continuoue via point
                try:
                    score_temp = 0
                    count = 0
                    for id,i in enumerate(t_i):
                        if id in [0]:
                            continue
                        try:
                            p, v, a = polyTrajEval(i, C[:,:,id-1], t_i[id-1])
                        except:
                            print(" via point %d incorrect returning value data type of polyTrajEval" %k)
                            return 0
                            
                        p1, v1, a1 = polyTrajEval(i, C[:,:,id], t_i[id])
                        count +=1
                        if np.absolute((np.array(p) - np.array(p1))).max() <= 0.001:
                            score_temp += 1
                        if np.absolute((np.array(v) - np.array(v1))).max() <= 0.001:
                            score_temp += 1
                        if np.absolute((np.array(a) - np.array(a1))).max() <= 0.001:
                            score_temp += 1

                    score_question += score_temp/(3*count)
                except:
                    print("polynomial trajectory error")


                try:
                    for i in t__:
                        p, v, a = polyTrajEval(i, C, t_i)
                        p_.append(p)
                        v_.append(v)
                        a_.append(a)
                    score_question += 1
                except:
                    print("polynomial trajectory error")

                if np.absolute(np.array(a_)).max() > 0.5:
                    print("max acceleration doesn't match the conditionnt")
                else:
                    score_question += 1
                
                if np.absolute(np.array(v_)).max() > 1.75:
                    print("max velocity doesn't match the condition")
                else:
                    score_question += 1

                fig, ax = plt.subplots(3)
                ax[0].plot(t__,p_)
                ax[0].set_title ("p-t")
                ax[1].plot(t__,v_)
                ax[1].set_title("v-t")
                ax[2].plot(t__,a_)
                ax[2].set_title("a-t")
                # plt.show()

                C = np.empty([3,3,3])
                C[:,:,0] = [[1, 1, 3],
                            [2, 2, 2],
                            [3, 3, 3]]
                C[:,:,1] = [[2, 1, 1],
                            [2, 2, 4],
                            [1, 3, 3]]
                C[:,:,2] = [[3, 1, 2],
                            [3, 2, 2],
                            [3, 3, 1]]
                p_ = []
                v_ = []
                a_ = []
                t_i = [0, 15, 32]
                t_ = [i/100 for i in range(50*100)]
                try:
                    for t in t_:
                        p, v, a = polyTrajEval(t, C, t_i)
                        p_.append(p)
                        v_.append(v)
                        a_.append(a)
                    score_question += 1
                except:
                    print("cubic case error")


                C = np.empty([3,4,3])
                C[:,:,0] = [[1, 1, 3, 3],
                            [2, 2, 2, 2],
                            [3, 3, 3, 2]]
                C[:,:,1] = [[2, 1, 1, 1],
                            [2, 2, 4, 2],
                            [3, 3, 1, 3]]
                C[:,:,2] = [[3, 1, 2, 2],
                            [3, 2, 2, 1],
                            [3, 3, 1, 2]]
                p_ = []
                v_ = []
                a_ = []
                t_i = [0, 15, 32]
                t_ = range(50*100)
                try:
                    for t in t_:
                        p, v, a = polyTrajEval(t/100, C, t_i)
                        p_.append(p)
                        v_.append(v)
                        a_.append(a)
                    score_question += 1
                except:
                    print("qudratic case error")
            
                print("via point {0} Score: {1:.2f}%".format(k, score_question*100/6))
                total_score += score_question/6
        except:
            print("via point %d incorrect returning value data type of HW4TrajGen" %k)
    return (total_score/5)

if __name__ == "__main__":
    data = load_json()
    print("Total Score: {0:.2f}%".format(scoreCalculate(data)*100))