# Efficient and High-Accuracy Secure Two-Party Protocols for a Class of Functions with Real-number Inputs



## Setup

For setup instructions, please refer to the README file located in the `SCI` folder.

We successfully completed the compilation on Ubuntu 22.04.5 LTS with Intel(R) Xeon(R) Platinum.


## Code Structure

The project is organized as follows:

- **/EZPC/SCI/tests**  
  Contains all ours related code, including implementations of activation functions and models.

- **/EzPC/SCI/tests/activation**  
  The **/EZPC/SCI/tests/activation** directory now includes our exulation functions:  
  - MW  
  - exp  
  - sin  
  - division  
  - softmax

## Running Tests

To run the unit tests in the `EZPC/` folder of our MPC Protocols, use the following command:

```bash
./SCI/build/bin/our-MW r=1 & ./SCI/build/bin/our-MW r=2
```

