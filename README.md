# 3N-MAC
Near Nodes Network MAC Protocol for Wireless Sensor Network

# Todo
- [ ] Implémenter CSMA/CA dans gnuradio
- [ ] Implémenter 3N-MAC


## To create a module using GNU Radio:
![Arch Installation](https://img.shields.io/badge/-Installing%20on%20Ubuntu-05122A?style=flat&logo=ubuntu&logoColor=FFFFFF&color=E95420)
```
sudo apt install gnuradio cmake libboost-all-dev
```
![Arch Installation](https://img.shields.io/badge/-Installing%20on%20Arch%20Linux-05122A?style=flat&logo=archlinux&logoColor=FFFFFF&color=1793D1)
```
pacman -S gnuradio python-cairo cmake boost
```

Then create the component:
```
gr_modtool newmod <name>
cd gr-<name>
gr_modtool add -t general <name>
```
Then choose Python and give the correct License.

## NS-3 Installation
1. Clone the repository
2. Install the following dependencies 
```sudo apt install g++ python3 python3-dev pkg-config sqlite3 cmake python3-setuptools git qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools gir1.2-goocanvas-2.0 python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython3 openmpi-bin openmpi-common openmpi-doc libopenmpi-dev autoconf cvs bzr unrar gsl-bin libgsl-dev libgslcblas0 wireshark tcpdump sqlite3 libsqlite3-dev libxml2 libxml2-dev libc6-dev libc6-dev-i386 libclang-dev llvm-dev automake python3-pip libxml2 libxml2-dev libboost-all-dev```

3. Download ns-3 archive from `https://www.nsnam.org/`
4. Untar : `tar jxvf ns-allinone-....tar.bz2`
5. `cd ns-allinone-.../`
6. `./build.py --enable-examples --enable-tests`

## Installation for graphical-sim (WIP)
1. Clone the repository
2. Create a new python env called *3n-mac*: `python -m venv ~/.virtualenvs/3n-mac`
3. Use the new python env : `source ~/.virtualenvs/3n-mac/bin/activate` if you use fish `source ~/.virtualenvs/3n-mac/bin/activate.fish`
4. Install the dependencies : `pip install -r requirements.txt`
5. Start the application : `python3 app.py`





### **1. When adding a new node:**

1. **Activation**:
   - The new node powers on and starts with mode **FD (Fast Discovery)**.
   - It sends *beacons* every second, to signal its presence.

2. **Neighbor discovery**:
   - Neighbor nodes already inside the network answer with a *welcoming beacon* containing :
     - Their address.
     - Their signal strength (RSSI).
     - Network information, necessary to join the cluster (e.g. security key or network ID).

3. **Best neighbor selection**:
   - To establish an initial connection, the new node selects the neighbor with the **best RSSI**.
   - It then proceeds to send a **connection** message to the selected neighbor.

4. **Connection approval**:
   - The neighbor checks whether the new node is approved (shared key authentification).
   - If everything checks out, the neighbor adds the new node to its routing table and transmits the information to the remaining nodes belonging to the network.

5. **Switching to SD mode**:
   - Once connected and stabilized, the new node is switched to **SD (Slow Discovery)** mode, to save on energy.

---

### **2. Organizing the network after adding a node:**

1. **Updating routes**:
   - All neighbor nodes update their routing table to include the new node.
   - Routes are recalculated dynamically, according to **RSSI** and nodes' energy load.

2. **Information propagation**:
   - The entire network is informed of the addition of a node, thanks to a controlled broadcast mechanism (to avoid overloads).

3. **Stabilization**:
   - Once routes are recalculated, the network should operate normally, with the new fully integrated node.

---

### **3. Sending a message from node A to B:**

1. **Route determining**:
   - Node A checks its **routing table** to find the best path to B.
   - If B is a direct neighbor, the message is directly sent.
   - Otherwise, the message is sent to the **next node on path** (determined by RSSI and priorities)

2. **Message transmitting**:
   - The message is transmitted from node to node, until reaching B.
   - Each intermediary node:
     - Checks its own routing table.
     - Forwards the message to the next node, with the **best RSSI** towards destination.

3. **Receipt acknowledgement**:
   - Once the message reaches B, a **receipt acknowledgement** is answered to A, following the reverse path.
   - If it is not received after a certain delay, A resends the acknowledgement, following another path.

---

### **4. What happens when a node disappears or defects?**

1. **Detection upon failure**:
   - Neighbors of a defect node can detect the absence of its *SD beacons*, after 3 consecutive cycles.

2. **Network update**:
   - Neighbors delete defect nodes from their routing table.
   - Routes are **dynamically reconfigured**. 

3. **Redundancy**:
   - Transiting messages are automatically redirected via other paths, if available.

---

### **5. Energy optimization and efficient communication:**

1. **Idle mode**:
   - Nodes which are neither emitting nor receiving messages turn to **idle mode**, to save their battery life.
   - They wake up only to listen for *SD beacons* or to emit/receive data.

2. **Reducing collisions** :
   - The protocol uses **CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)**:
     - Each node checks whether the channel is free or not, before emitting a message.
     - When a collision is detected, emission is reproduced after a random delay.


### **Summary of the main stages:**

- **Adding a node**: The new node discovers its neignbors, then connects to the **best**, and it is finally integrated to the network.
- **Sending a message**: Messages follow the path with the best RSSI, with each node acting as a relay, if necessary.
- **Dealing with defects**: When a node disappears, routes are automatically recalculated, to ensure connectivity.
- **Optimizing energy consumption**: Nodes work on idle modes and optimized transmission cycles, to reduce their energy consumption.
