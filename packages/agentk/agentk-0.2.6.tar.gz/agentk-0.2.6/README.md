# "k"

## TLDR;

Install the "k" by either doing: 

	pip install agentk

(Yes, ^^ it is written in python and your OS needs to have recent version 2 or 3)

or copying it in some bin folder on your PATH and running `pip install -r requirements.txt`

---

 > "A person is smart. People are dumb, panicky, dangerous animals, and you know it." -- Agent K

#### "AGENT" K is a complete minimalistic kubectl "doner"-wrap

Obviously, as a short-hand wrapper, **k** can do everything **kubectl** already can, but it is (a) shorter and (b) adds few tricks like merging configs and switching contexts .. (k) feeds back to the *kubectl* command-line those args which it does not want to intercept or handle.

## Usage

The following is equivalent:

	kubectl get pods --all-namespaces
	k get pods -A
	k p -A


### Switching context

Argument-free invocation prompts for context switch options between multiple cluster contexts found in `~/.kube/config`:

	k


## Develop

To remind, you can do `pip install -e .` in order to utilize developer mode.
