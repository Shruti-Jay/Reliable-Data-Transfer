# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the receiver in a Go-Back-N data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_five
from packet import send_ack
from packet import packet 


class R_receiver:
    ''' Represents the Receiver in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Receiver. '''

        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.

        # The sequence number of next packet that is expected to be received
        # from the Sender.
        self.seqnum = 0
        # This should be used as the first argument to to_layer_five() and 
        # send_ack().
        self.entity = 'R'

        # Variables to track function usage
       

        return

    def R_input(self, received_packet):
        ''' 
        The Receiver received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Sender.
        ''' 
        # Verify the received packet's checksum
        if received_packet.get_checksum() != received_packet.checksum:
            # Corrupted packet
            print("Corrupted packet received.")
            sim.corruptedData += 1
            self.stats['get_checksum'] += 1
            return

        # Packet is not corrupted, process sequence number
        seqnum = received_packet.seqnum

        if seqnum == self.seqnum:
            # Correct packet received, deliver to layer 5
            to_layer_five(self.entity, received_packet.payload)
            self.stats['toLayerFive'] += 1

            # Send acknowledgment
            ack_pkt = packet(seqnum, 0, None)
            ack_pkt.checksum = ack_pkt.get_checksum()
            send_ack(self.entity, ack_pkt.acknum)
            self.stats['send_ack'] += 1

            # Update sequence number for the next expected packet
            self.seqnum = (self.seqnum + 1) % 8
        else:
            # Out-of-order packet received, discard
            print("Out-of-order packet received. Discarding.")
        
        return

# Instantiate the receiver
b = R_receiver()
