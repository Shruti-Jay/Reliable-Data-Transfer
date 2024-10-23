# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the sender in a Stop-and-Wait data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *

class S_sender:
    ''' Represents the Sender in the Stop-and-Wait protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.
        
        # For Stop-and-Wait, the state can be "WAIT_LAYER5" or "WAIT_ACK".
            # "WAIT_LAYER5" is the state where the Sender waits for messages 
            # from the application layer (layer 5).
            # "WAIT_ACK" is the state where the Sender waits to receive an 
            # ACK from the Receiver.
        self.state = "WAIT_LAYER5"
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'

        # TODO: Initialize any other useful class variables you can think of.
        self.message = None

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

        sim.totalMsgSent += 1
        # Follow the finite state machine (FSM) to know the exact actions that 
        # should be taken in each state to send this message to the receiver and 
        # review section 2.5.2 Software Interfaces in the Project Instructions 
        # for how to use each method.
        # TODO: 
        # 1) Verify the current state of the Sender to make sure it should
            # actually send the message to the Receiver.
        # 2) Send the message 
            # Use the message when constructing the new packet.
            # new_packet = packet(seqnum = self.seq, payload = message)
            # Send the packet to the Receiver.
            # to_layer_three(self.entity, new_packet)
        # 3) Start the timer (you only need one timer)
        # 4) Check what you need to do to handle if the packet you sent is 
            # lost or corrupted. 
        # 5) Do not forget to update the class variables and the statistics 
        # counters accordingly.

        if self.state == "WAIT_LAYER5":
            # Construct a new packet with the current sequence number and message
            new_packet = packet(seqnum=self.seq, payload=message)
            # Send the packet to layer 3
            to_layer_three(self.entity, new_packet)
            # Start the timer for packet timeout
            evl.start_timer(self.entity, self.estimated_rtt)
            # Transition to the next state
            self.state = "WAIT_ACK"
        elif self.state  == "WAIT_ACK":
            # Increment dropped counter for data packets
            sim.droppedData += 1
            print(f"waiting for ack, new message is dropped: {message}")
            # Do not send the packet, as the sender is waiting for an ACK
            # Instead, you may choose to raise an error or handle it differently
        self.message = message 


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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: Verify the current state of the Sender to make sure it should 
        # actually process the received packet, the checksum to make sure that
        # received packet is uncorrupted, and the acknowledgment number to see
        # whether it is the expected one.
        
        if self.state == "WAIT_ACK":
            if (received_packet.checksum == received_packet.get_checksum() and
                    received_packet.acknum == self.seq):
                # Increment retransmitted data counter
                sim.retransmittedData += 1
                # Received packet is valid and has the expected acknowledgment number
                # Stop the timer
                evl.remove_timer(self.entity)
                # Transition back to the "WAIT_LAYER5" state
                self.state = "WAIT_LAYER5"
                # Increment sequence number for the next packet
                self.seq += 1
                


        return


    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that the ACK for the most recently 
            sent packet wasn't received by the Sender in time, so the packet 
            needs to be retransmitted. '''
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces and 2.5.4 Helpful Hints in the Project Instructions
        # for how to use each method and how to handle timers.
        # TODO: Verify the current state of the Sender to make sure it should 
        # actually handle the timeout. Retransmit the most recently sent packet 
        # and start the timer again.
        
        if self.state == "WAIT_ACK":
        # Timeout occurred, retransmit the packet
            if self.message is not None:
                # Increment retransmitted data counter
                sim.retransmittedData += 1
            # Construct the packet with the same sequence number and payload
                retransmit_packet = packet(seqnum=self.seq, payload=self.message)
            # Resend the packet to layer 3
                to_layer_three(self.entity, retransmit_packet)
            # Restart the timer for packet timeout
                evl.start_timer(self.entity, self.estimated_rtt)

                self.message = None
            else:
                print("No message to retransmit.") #for private checking
                sim.retransmittedAck += 1

        return

a = S_sender()