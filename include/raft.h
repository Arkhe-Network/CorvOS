#ifndef RAFT_H
#define RAFT_H

typedef enum {
    FOLLOWER,
    CANDIDATE,
    LEADER
} NodeState;

typedef struct {
    int term;
    int votedFor;
    NodeState state;
} RaftNode;

void raft_init(RaftNode *node);
void raft_request_vote(RaftNode *node);
void raft_append_entries(RaftNode *node);
void raft_run(RaftNode *node);

#endif