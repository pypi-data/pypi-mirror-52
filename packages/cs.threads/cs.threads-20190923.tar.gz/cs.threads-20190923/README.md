threading and communication/synchronisation conveniences


*Latest release 20190923*:
Remove dependence on cs.obj.

Thread related convenience classes and functions.

## Class `AdjustableSemaphore`

A semaphore whose value may be tuned after instantiation.

## Function `bg(func, daemon=None, name=None, no_start=False, no_logexc=False, args=None, kwargs=None)`

Dispatch the callable `func` in its own `Thread`;
return the `Thread`.

Parameters:
* `func`: a callable for the `Thread` target.
* `daemon`: optional argument specifying the `.daemon` attribute.
* `name`: optional argument specifying the `Thread` name,
  default: the name of `func`.
* `no_start`: optional argument, default `False`.
  If true, do not start the `Thread`.
* `no_logexc`: if false (default `False`), wrap `func` in `@logexc`.
* `args`, `kwargs`: passed to the `Thread` constructor

## Class `LockableMixin`

Trite mixin to control access to an object via its ._lock attribute.
Exposes the ._lock as the property .lock.
Presents a context manager interface for obtaining an object's lock.

## Function `locked(func)`

A decorator for monitor functions that must run within a lock.
Relies upon a ._lock attribute for locking.

## Function `locked_property(func, lock_name='_lock', prop_name=None, unset_object=None)`

A thread safe property whose value is cached.
The lock is taken if the value needs to computed.

## Class `PriorityLock`

A priority based mutex.

A priority based mutex which is acquired by and released to waiters
in priority order.

The initialiser sets a default priority, itself defaulting to `0`.

The `acquire()` method accepts an optional `priority` value
which specifies the priority of the acquire request;
lower values have higher priorities.
`acquire` returns a new `PriorityLockSubLock`.

Note that internally this allocates a `threading.Lock` per acquirer.

When `acquire is called, if the `PriorityLock` is taken
then the acquirer blocks on their personal `Lock`.

When `release()` is called the highest priority `Lock` is released.

Within a priority level `acquire`s are served in FIFO order.

Used as a context manager, the mutex is obtained at the default priority.

The `priority()` method offers a context manager
with a specified priority.

### Method `PriorityLock.__init__(self, default_priority=0, name=None)`

Initialise the `PriorityLock`.

Parameters:
* `default_priority`: the default `acquire` priority,
  default `0`.
* `name`: optional identifying name

## Function `via(cmanager, func, *a, **kw)`

Return a callable that calls the supplied `func` inside a
with statement using the context manager `cmanager`.
This intended use case is aimed at deferred function calls.

## Class `WorkerThreadPool`

MRO: `cs.resources.MultiOpenMixin`  
A pool of worker threads to run functions.

### Method `WorkerThreadPool.__init__(self, name=None, max_spare=4)`

Initialise the WorkerThreadPool.

Parameters:
* `name`: optional name for the pool
* `max_spare`: maximum size of each idle pool (daemon and non-daemon)

## Class `WTPoolEntry`

MRO: `builtins.tuple`  
WTPoolEntry(thread, queue)



# Release Log

*Release 20190923*:
Remove dependence on cs.obj.

*Release 20190921*:
New PriorityLock class for a mutex which releases in (priority,fifo) order.

*Release 20190812*:
bg: compute default name before wrapping `func` in @logexc.

*Release 20190729*:
bg: provide default `name`, run callable inside Pfx, add optional no_logexc=False param preventing @logec wrapper if true.

*Release 20190422*:
bg(): new optional `no_start=False` keyword argument, preventing Thread.start if true

*Release 20190102*:
Drop some unused classes.
New LockableMixin, presenting a context manager and a .lock property.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
Replace bare "excepts" with "except BaseException".
Doc updates. Other minor improvements.

*Release 20150115*:
First PyPI release.
