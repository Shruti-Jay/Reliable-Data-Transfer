from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *
from circular_buffer import circular_buffer

class S_sender:
    ''' Represents the Sender in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.
        
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'
        # The circular buffer that will store any outstanding and 
        # unacknowledged packets.
        self.c_b = circular_buffer(8)

        # Variables to track function usage
        self.stats = {
            'toLayerThree': 0,
            'start_timer': 0,
            'get_checksum': 0,
            'toLayerFive': 0,
            'isfull': 0,
            'push': 0,
            'pop': 0,
            'readall': 0
        }

        # TODO: Initialize any other useful class variables you can think of.

        return

    def S_output(self, message):
        '''
        The Sender received a message from layer 5, so it should try to create
        a packet containing the message and send it to layer 3. 
        
        Parameters
        ----------
        - message : msg
            - The message the Sender received from layer 5.
        '''
        # Check if the circular buffer is full
        if self.c_b.isfull():
            self.stats['isfull'] += 1
            print("Circular buffer is full. Message dropped.")
            # Update statistics counters
            sim.droppedData += 1
            return

        # Create a packet containing the message
        pkt = packet(self.seq, 0, message)
        # Compute checksum
        pkt.checksum = pkt.get_checksum()
        # Push the packet into the circular buffer
        self.c_b.push(pkt)
        self.stats['push'] += 1

        # Send the packet to layer 3
        to_layer_three(self.entity, pkt)
        self.stats['toLayerThree'] += 1

        # Start the timer if needed
        if self.seq == 0:
            evl.start_timer(self.entity, self.estimated_rtt)
            self.stats['start_timer'] += 1

        # Update sequence number for the next packet
        self.seq = (self.seq + 1) % 8

        # Update statistics counters
        sim.totalMsgSent += 1

        return    
        
            
    def S_input(self, received_packet):
        '''
        The Sender received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Receiver.
        '''
        # Verify the received packet's checksum
        if received_packet.get_checksum() != received_packet.checksum:
            # Corrupted packet
            print("Corrupted packet received.")
            sim.corruptedData += 1
            self.stats['get_checksum'] += 1
            return

        # Packet is not corrupted, process acknowledgment number
        acknum = received_packet.acknum

        # Update circular buffer based on the received acknowledgment number
        while not self.c_b.isfull():
            pkt = self.c_b.pop()
            self.stats['pop'] += 1
            if pkt.seqnum == acknum:
                # Packet acknowledged
                break

        # Update statistics counters
        sim.retransmittedData += self.c_b.count

        return

    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that an ACK for any of the most 
            recently sent packets wasn't received by the Sender in time, so 
            all currently outstanding and unacknowledged packet needs to be 
            retransmitted. '''
        # Retransmit all unacknowledged packets in the circular buffer
        packets = self.c_b.read_all()
        self.stats['readall'] += 1
        for pkt in packets:
            to_layer_three(self.entity, pkt)
            self.stats['toLayerThree'] += 1

        # Restart the timer
        evl.start_timer(self.entity, self.estimated_rtt)
        self.stats['start_timer'] += 1

        # Update statistics counters
        sim.retransmittedData += len(packets)
        
        return

# Instantiate the sender
a = S_sender()
