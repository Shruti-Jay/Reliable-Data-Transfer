## Project Overview


This project is a culmination of the skills and knowledge acquired in Python programming and different protocols throughout the course of the semester in CSCI 4211 Introduction to Computer Networks.
The goal of this project is to prove my reliable data transfer (“RDT”) protocol implemetation skills. This project implements ones similar to rdt3.0 (Alternating-Bit-Protocol or
Stop-and-Wait) and Go-Back-N. This projects contains sending and receiving transport-level code for implementing an RDT protocol. Implemented routines in the source code to support the RDT from the Sender to the Receiver (only one direction) with a
simulated lossy and noisy channel. 

### Phase 1
The Stop-and-Wait protocol is a simple flow control mechanism used in data communication.
In this implementation, the protocol is used to transfer data from a sender to a receiver in a
computer network.

- Sender:
Sender (S_sender class):
The sender waits for messages from the application layer (layer 5) in the
"WAIT_LAYER5" state. When a message is received from layer 5 (S_output function), the
sender creates a packet with the current sequence number and sends it to the receiver via layer
3.After sending the packet, the sender transitions to the "WAIT_ACK" state and starts a timer for
packet timeout. Upon receiving an ACK from the receiver (S_input function), the sender verifies
the acknowledgment number and transitions back to the "WAIT_LAYER5" state.
If the timer expires before receiving an ACK (S_handle_timer function), the sender retransmits
the packet and restarts the timer.

- Receiver:
The receiver waits for packets from layer 3.Upon receiving a packet from layer 3
(R_input function), the receiver verifies the checksum and the sequence number to ensure the
packet's integrity and correctness.If the received packet is valid, the receiver passes the
payload to layer 5 and sends an ACK to the sender with the acknowledgment number.
The receiver then updates its expected sequence number.If the received packet is corrupted, it
is discarded, and appropriate counters are updated.

- S_output(message): Handles the message received from layer 5. It constructs a packet
with the message and sends it to layer 3.
- S_input(received_packet): Processes the packet received from layer 3. It verifies the
ACK number and handles it accordingly.
- S_handle_timer(): Manages the expiration of the sender's timer. It retransmits the packet
if no ACK is received within the timeout period.
- R_input(received_packet): Deals with the packet received from layer 3 at the receiver's
end. It verifies the packet's integrity, sends ACK if the packet is correct, and updates the
sequence number.
- Initialization functions: Initializes relevant class variables and states for both sender and
receiver.
- Additional Data Structures/Fields/Methods:
Message Buffer (self.message): Stores the message being sent by the sender, allowing
for retransmission if needed.

### Phase 2
The Go-Back-N (GBN) protocol is a sliding window protocol used for reliable data transfer in
computer networks. In this implementation, the GBN protocol is used to transfer data from a
sender to a receiver.

- The Go-Back-N (GBN) protocol is a sliding window protocol used for reliable data transfer in
computer networks. In this implementation, the GBN protocol is used to transfer data from a
sender to a receiver.
- Sender: The sender (GBN_Sender.py) waits for messages from the application layer (layer 5) in the
"WAIT_LAYER5" state. Upon receiving a message from layer 5 (S_output function), the sender creates packets with
sequence numbers and sends them to the receiver via layer 3.  After sending packets, the sender waits for ACKs from the receiver in the "WAIT_ACK"
state. Upon receiving ACKs, the sender updates the window and sends new packets or
retransmits packets as necessary.
- Receiver: The receiver (GBN_Receiver.py) waits for packets from layer 3. Upon receiving packets from layer 3 (R_input function), the receiver verifies the checksum
and the sequence number to ensure packet integrity and correctness. If the received packet is valid, the receiver sends an ACK to the sender with the
acknowledgment number. The receiver then updates its expected sequence number. If the received packet is corrupted or out of order, it is discarded, and appropriate counters
are updated.

- S_output(message): Handles the message received from layer 5. It constructs packets with
messages and sends them to layer 3.
- S_input(received_packet): Processes packets received from layer 3. It verifies ACK
numbers and handles them accordingly.
- S_handle_timer(): Manages the expiration of the sender's timer. It retransmits packets if no
ACKs are received within the timeout period.
- R_input(received_packet): Deals with packets received from layer 3 at the receiver's end. It
verifies packet integrity, sends ACKs for correct packets, and updates the sequence number.
- Initialization functions: Initializes relevant class variables and states for both sender and
receiver.
- Circular Buffer: Used for storing outstanding and unacknowledged packets at the sender's
end.
- Event List: Manages events in the simulation, such as timeouts and packet arrivals.
- Packet and Message Classes: Represent packets and messages exchanged between
sender and receiver

