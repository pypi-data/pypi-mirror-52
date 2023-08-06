# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:30:45 2019

@author: cham
"""

#%%
%pylab

#%%
x = np.linspace(1, 2, 100)
y = x*1.2+np.random.randn(*x.shape)*1+.1
yerr = y*0+.1
                         
#%%
figure()
plot(x, y,'.')

#%%

def f_model(p, x):
    """ p = [a, b] """
    a, b = p
    return a*x+b

def costfun(p, xobs, yobs, yobserr):
    return -np.sum(((f_model(p, xobs)-yobs)/yobserr)**2)/2


#%%
from emcee import EnsembleSampler
sampler = EnsembleSampler(8, 2, costfun, args=[x, y, yerr])
#%%
""" initial positions """
p0 = np.random.randn(8, 2)

""" burn-in """
pos, lnprob, rstate = sampler.run_mcmc(p0, 1000)
figure();plot(sampler.chain[:,:, 0].T)
""" T=transpost"""
""" run mcmc """
sampler.reset()
sampler.run_mcmc(pos, 2000)
figure();plot(sampler.chain[:,:, 0].T)

#%%

from corner import corner
corner(sampler.flatchain)

#%%
def run_mcmc(obs, obs_err=0, mod_err=0, obs_tag=None, p0=None, 
             n_burnin=(100, 100), n_step=1000, 
             lnlike=None, lnprior=None,
             lnlike_kwargs={}, lnprior_kwargs={},
             pos_eps=.1, full=True, shrink="max"):
    """ run MCMC for (obs, obs_err, obs_weight)

    Parameters
    ----------
    obs:
        observable
    obs_err:
        error of observation
    obs_tag:
        array(size(obs), 1 for good, 0 for bad.
    p0:
        initial points
    n_burnin:
        int/sequence, do 1 or multiple times of burn in process
    n_step:
        running step
    lnlike:
        lnlike(x, *args) is the log likelihood function
    lnprior:
        lnpost(x) is the log prior
    pos_eps:
        random magnitude for starting position
    full:
        if True, return sampler, pos, prob, state
        otherwise, return sampler
    shrink:
        default "max": shrink to the maximum likelihood position

    Return
    ------
    EnsembleSampler instance

    """
    if obs_tag is None:
        # default obs_weight
        obs_tag = np.isfinite(obs)
    else:
        obs_tag = np.isfinite(obs) & obs_tag
    # cope with bad obs
    if np.sum(obs_tag) == 0:
        return None

    if p0 is None:
        # do best match for starting position
        p0 = self.best_match(obs, obs_err)
        print("@Regli.best_match: ", p0)

    if lnlike is None:
        # default gaussian likelihood function
        lnlike = default_lnlike
        print("@Regli: using the default gaussian *lnlike* function...")

    if lnprior is None:
        # no prior is specified
        lnpost = lnlike
        print("@Regli: No prior is adopted ...")
    else:
        # use user-defined prior
        print("@Regli: using user-defined *lnprior* function...")

        def lnpost(*_args, **_kwargs):
            lnpost_value = np.float(
                lnprior(_args[0], **_kwargs["lnprior_kwargs"])) + \
                           lnlike(*_args, **_kwargs["lnlike_kwargs"])
            if np.isfinite(lnpost_value):
                return lnpost_value
            else:
                return -np.inf

    # set parameters for sampler
    ndim = self.ndim
    nwalkers = 2 * ndim

    # initiate sampler
    sampler = EnsembleSampler(nwalkers, ndim, lnpostfn=lnpost,
                              args=(self, obs, obs_err, obs_tag),
                              kwargs=dict(lnprior_kwargs=lnprior_kwargs,
                                          lnlike_kwargs=lnlike_kwargs))

    # generate random starting positions
    pos0 = rand_pos(p0, nwalkers=nwalkers, eps=pos_eps)

    if isinstance(n_burnin, collections.Iterable):
        # [o] multiple burn-ins
        for n_burnin_ in n_burnin:
            # run mcmc
            print("@Regli: running burn-in [{}]...".format(n_burnin_))
            pos, prob, state = sampler.run_mcmc(pos0, n_burnin_)

            # shrink to a new position
            if shrink == "max":
                p1 = sampler.flatchain[np.argmax(sampler.flatlnprobability)]
            else:
                p1 = np.median(pos, axis=0)
            pos_std = np.std(sampler.flatchain, axis=0) * 0.5

            # reset sampler
            sampler.reset()

            # randomly generate new start position
            pos0 = rand_pos(p1, nwalkers=nwalkers, eps=pos_std)

    else:
        # [o] single burn-in
        # run mcmc
        print("@Regli: running burn-in [{}]...".format(n_burnin))
        pos, prob, state = sampler.run_mcmc(pos0, n_burnin)

        # shrink to a new position
        if shrink == "max":
            p1 = sampler.flatchain[np.argmax(sampler.flatlnprobability)]
        else:
            p1 = np.median(pos, axis=0)
        pos_std = np.std(sampler.flatchain, axis=0) * 0.5

        # reset sampler
        sampler.reset()

        # randomly generate new start position
        pos0 = rand_pos(p1, nwalkers=nwalkers, eps=pos_std)

    # run mcmc
    print("@Regli: running chains [{}]...".format(n_step))
    pos, prob, state = sampler.run_mcmc(pos0, n_step)

    if full:
        # return full result
        return sampler, pos, prob, state
    else:
        # return sampler only
        return sampler