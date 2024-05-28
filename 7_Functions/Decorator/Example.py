# def exec_log(func):
#     @wraps(func)
#     def inner(*args, **kwargs):
#         start_time = time.perf_counter()
#         ret = func(*args,**kwargs)
#         if args and kwargs:
#             logger.info("Completed executing {}({},{})".format(func.__qualname__,args,kwargs))
#         elif args:
#             logger.info("Completed executing {}({})".format(func.__qualname__,args))
#         else:
#             logger.info("Completed executing {}({})".format(func.__qualname__,kwargs))
#         run_time = time.perf_counter()   - start_time
#         logger.info("The program returned result {}".format(ret))
#         logger.info("Finished {}() in {} secs".format(func.__qualname__,run_time))
#         return ret
#     return inner