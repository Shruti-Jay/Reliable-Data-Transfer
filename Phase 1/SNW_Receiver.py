# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the receiver in a Stop-and-Wait data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_five
from packet import send_ack

class R_receiver:
    ''' Represents the Receiver in the Stop-and-Wait protocol. '''
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
        
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: If the packet is received correctly, pass it to layer 5 using:
        # to_layer_five(self.entity, received_packet.payload.data)
        # Send an ACK packet to the Sender and Update seqnum to the next expected 
        # sequence number.
        
        if (received_packet.checksum == received_packet.get_checksum() and
                received_packet.seqnum == self.seqnum):
            sim.retransmittedAck += 1
            # Pass the payload of the packet to layer 5
            sim.to_layer_five(self.entity, received_packet.payload.data)
            # Send an ACK packet to the sender with the acknowledgment number
            send_ack(self.entity, received_packet.seqnum)
            # Update seqnum to the next expected sequence number
            self.seqnum += 1
            #increment the total number of messages sent 
            sim.totalMsgSent += 1
        else:
            sim.corruptedData += 1 #increment corrupted data count
        
        if received_packet.checksum != received_packet.get_checksum():
            sim.retransmittedAck += 1

        # Increment dropped counter for ACK packets
        if received_packet.checksum == -1:
            sim.droppedAck += 1

            

            
        return

b = R_receiver()