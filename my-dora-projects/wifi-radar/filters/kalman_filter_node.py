import numpy as np
import random
from dora import Node
import time
import logging


def rssi_to_distance(rssi, tx_power=-59, n=2.7):
    """
    Params:
    - rssi: the signal strength reading that was measured
    - tx_power: known signal strength at exactly 1 meter distance
              typically around -59 dBm for phones
              this is a calibration constant
    - n: path loss exponent
              describes how fast signal weakens with distance
              2.0   = free space, open air, no obstacles
              2.7   = typical indoors
              3.5   = heavy obstruction, lots of walls
    """
    distance = 10 ** ((tx_power - rssi) / (10 * n))
    return distance


def main():

    node = Node()

    # state extrapolation
    initial_rssi = 0
    initial_speed = 0
    prev_time = time.time()

    state_matrix = np.array([[initial_rssi], [initial_speed]])

    # n,n
    confirmed_covariance_matrix = np.array([[5, 0], [0, 25]])

    i = np.array([[1, 0], [0, 1]])

    measurement_covariance_matrix = np.array([[1]])

    # convert the variables we are tracking to match the variables actually measured
    observation_matrix = np.array([[1, 0]])

    # wait for sensor data inputs
    for event in node:

        event_type = event["type"]
        if event_type == "INPUT":
            event_id = event["id"]
            if event_id == "rssi_data":
                data = event["value"].to_pylist()

                # current_time = random.uniform(1,3)
                # current_rssi = -random.randint(65, 80)
                # extract data received from sensor (sensor node)
                current_rssi = data[0]
                current_time = data[1]

                # convert rssi to distance estimate
                measured_distance = rssi_to_distance(current_rssi)

                # first distance must be set to the first measured rssi
                if state_matrix[0][0] == 0:
                    state_matrix[0][0] = measured_distance
                print("current time: ", current_time, "current_rssi: ", current_rssi)

                # calculate the change in time from sensor readings
                change_in_time = current_time - prev_time
                prev_time = current_time

                # state transition matrix must update the time between sensor readings
                state_transition_matrix = np.array([[1, change_in_time], [0, 1]])

                # apply a noise variance of 1 m²/s⁴ (acceleration variance)
                noise_variance = 1
                # noise matrix: utilizes the variance of acceleration that someone may walk at a unpredictable pace
                # acceleration variance is applied to variables we are tracking (position, velocity, position and velocity) The noise matrix is the variance of position, velocity with relation to acceleration
                noise_matrix = np.array(
                    [
                        [(change_in_time**4) / 4, (change_in_time**3) / 2],
                        [(change_in_time**3) / 2, change_in_time**2],
                    ]
                )
                noise_matrix *= noise_variance

                # predict the values of the state matrix
                predicted_state = np.dot(state_transition_matrix, state_matrix)

                measured_distance_matrix = np.array([measured_distance])

                # create the covariance extrapolation (n,n+1) for the prediction (what we put in)
                prediction_covariance_extrapolation = np.dot(
                    state_transition_matrix, confirmed_covariance_matrix
                )
                prediction_covariance_extrapolation = np.dot(
                    prediction_covariance_extrapolation, state_transition_matrix.T
                )
                print("covariance extrapolation: ", prediction_covariance_extrapolation)

                # sum the covariance prediction with process noise
                prediction_covariance_extrapolation = np.add(
                    prediction_covariance_extrapolation, noise_matrix
                )

                # calculate kalman gain (multi-variate case) utilizing prediction and measured covariance matrices and finds the optimal blend to minimize variance of the updated estimate
                kalman_gain = np.dot(
                    np.dot(prediction_covariance_extrapolation, observation_matrix.T),
                    np.linalg.inv(
                        np.add(
                            np.dot(
                                observation_matrix,
                                np.dot(prediction_covariance_extrapolation, observation_matrix.T),
                            ),
                            measurement_covariance_matrix,
                        )
                    ),
                )
                print("kalman gain: ", kalman_gain)

                # update the state based on the kalman gain to apply the best estimate to the state
                updated_state = np.add(
                    predicted_state,
                    np.dot(
                        kalman_gain,
                        np.subtract(
                            measured_distance_matrix,
                            (np.dot(observation_matrix, predicted_state)),
                        ),
                    ),
                )
                print("state update: ", updated_state)

                # state matrix must be updated forward for the next iteration
                state_matrix = updated_state

                # update the confirmed estimate covariance (pn,n) (what we get out)
                covariance_update = np.dot(
                    np.subtract(i, np.dot(kalman_gain, observation_matrix)),
                    prediction_covariance_extrapolation,
                )
                confirmed_covariance_matrix = covariance_update
                print("confirmed covariance matrix: ", confirmed_covariance_matrix)

        elif event_type == "STOP":
            logging.info("Stopping early, no more data to process")

if __name__ == "__main__":
    main()
