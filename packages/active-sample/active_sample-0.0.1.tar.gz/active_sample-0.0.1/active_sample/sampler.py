class ActiveSampler(object):
    def __init__(self, num_sample_round=20, majority_ratio=5):
        self.num_sample_round = num_sample_round
        self.majority_ratio = majority_ratio
        
    def select(self, x, y, minority_label=1):
        self.minority_label = minority_label
        
        self.minority = x[y == self.minority_label]
        self.majority = x[y != self.minority_label]
        
        self.minority_num = self.minority.shape[0]
        self.round_batch = ceil(self.minority_num / self.num_sample_round)
        
        self.sampled_x = pd.DataFrame()
        self.sampled_y = pd.Series()
        self.false_prob_dist = None
        
        for i in range(self.num_sample_round):
            min_bth_idxes = np.random.choice(self.minority.index.tolist(),
                                                size=min(self.round_batch, self.minority.shape[0]),
                                                replace=False)
            maj_bth_idxes = np.random.choice(self.majority.index.tolist(),
                                                 size=min(self.round_batch*self.majority_ratio, self.majority.shape[0]),
                                                 replace=False,
                                                 p=self.false_prob_dist)

            self.sampled_x = self.sampled_x.append(self.minority.loc[min_bth_idxes])
            self.sampled_x = self.sampled_x.append(self.majority.loc[maj_bth_idxes])
            self.sampled_y = self.sampled_y.append(y.loc[min_bth_idxes])
            self.sampled_y = self.sampled_y.append(y.loc[maj_bth_idxes])

            self.minority = self.minority.drop(index=min_bth_idxes)
            self.majority = self.majority.drop(index=maj_bth_idxes)
            yield self.sampled_x, self.sampled_y
    
    def update_dist(self, scores):
        """
        The shape of scores need to be as x in select func
        """
        sampled_score = scores[self.majority.index]
        self.false_prob_dist = sampled_score / np.sum(sampled_score)
