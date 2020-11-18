import torch
import numpy as np
from torch.distributions.independent import Independent
from torch.distributions.multivariate_normal import MultivariateNormal
from torch.distributions.normal import Normal
"""

Exercise 1.1: Diagonal Gaussian Likelihood

Write a function that takes in PyTorch Tensors for the means and 
log stds of a batch of diagonal Gaussian distributions, along with a 
PyTorch Tensor for (previously-generated) samples from those 
distributions, and returns a Tensor containing the log 
likelihoods of those samples.

"""

def gaussian_likelihood(x, mu, log_std):
    """
    Args:
        x: Tensor with shape [batch, dim]
        mu: Tensor with shape [batch, dim]
        log_std: Tensor with shape [batch, dim] or [dim]

    Returns:
        Tensor with shape [batch]
    """ 

    # Correct answer based on solution presented by spinningup
#    EPS = 1e-8
#    dims = x.size(-1)
#    last_term = - 0.5 * dims * np.log(2*np.pi)
#    
#    inner_exp = ((x-mu)/(torch.exp(log_std)+EPS))**2 + 2 * log_std 
#    sum_exp = -0.5 * ( inner_exp.sum(-1))
    
    

#    print (log_std.size())
    mvn = Normal(mu, torch.exp(log_std))
    diag_mvn = Independent(mvn,1)
    ans = diag_mvn.log_prob(x)
    #print (ans)
    #for xi in x:
    #  log_prob = diag_mvn.log_prob(xi)
    #  print (xi, log_prob)
    #  ans.append(xi)
    #######################
    #                     #
    #   YOUR CODE HERE    #
    #                     #
    #######################
    # return sum_exp + last_term
    return ans

if __name__ == '__main__':
    """
    Run this file to verify your solution.
    """
    from spinup.exercises.pytorch.problem_set_1_solutions import exercise1_1_soln
    from spinup.exercises.common import print_result

    batch_size = 32
    dim = 10

    x = torch.rand(batch_size, dim)
    mu = torch.rand(batch_size, dim)
    log_std = torch.rand(dim)

    your_gaussian_likelihood = gaussian_likelihood(x, mu, log_std)
    true_gaussian_likelihood = exercise1_1_soln.gaussian_likelihood(x, mu, log_std)

    your_result = your_gaussian_likelihood.detach().numpy()
    true_result = true_gaussian_likelihood.detach().numpy()

    print ('My answer:', your_result)
    print ('True Result:', true_result)
    correct = np.allclose(your_result, true_result)
    print_result(correct)
