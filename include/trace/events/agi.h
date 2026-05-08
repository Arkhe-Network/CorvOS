/* include/trace/events/agi.h */
#ifndef _TRACE_AGI_H
#define _TRACE_AGI_H

/* Placeholder for tracepoints */
static inline void trace_agi_init(void) {}
static inline void trace_agi_exit(void) {}
static inline void trace_agi_inference(u64 graph_id, u64 target_coherence, u32 num_observables, int ret) {}
static inline void trace_sched_coherence_enqueue(int cpu, pid_t pid, s64 impact) {}
static inline void trace_sched_coherence_dequeue(int cpu, pid_t pid) {}
static inline void trace_sched_coherence_pick(int cpu, pid_t pid, s64 impact) {}

#endif /* _TRACE_AGI_H */