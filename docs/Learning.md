# Learning

## Recommendation

#### Recommender Systems: Beyond Machine Learning. J. Konstan
"This talk takes a look at successes and failures in moving beyond basic machine 
learning approaches to recommender systems to emphasize factors tied to user behavior and 
experience. Along the way, we explore approaches to combining human-centered evaluation 
with data mining and machine learning techniques."

* Optimization by narrowing the search space of choices
  * Filtering (spam e.g.)
  * Recommendations (top-n list, expert advice)
  * Price/value prediction (hotel, restaurant stars)
* Types of personalization
  * Generic (e.g. billboard top songs)
  * Demographic (based on age/gender)
  * Contextual (e.g. books similar to ones you're looking at)
  * Persistent (match to a profile of activity/info)
    * This has a dual in building a community (e.g. meetups, Facebook groups)
* Recommendation approaches
  * Manual/marketing
  * Summary stats
  * Associations (contextual, statistical)
  * Content-based (learning from single-user profiles e.g. Netflix recs)
  * Collaborative techniques (learning from other)
    * Attractive when the problem space isn't well-defined either
* User-user collaborative filtering
  * Clustering users/products based on similarity of outcomes
  * Recommendation matrix can be analyzed in two ways:
    * Latent factor model. SVD to decompose the matrix. Or using optimization to find factors without decompsing the matrix.
    * Online learning. Reinforcement, multi-armed bandit. 
* Problems
  * Poor recommendations because of ... over
* What's a useful recommendation?
  * Accuracy - likelihood of adoption
  * Novelty - something unique
  * Diversity - 
  * Personalization -
  * Explainability - story to a recommendation
  * Business value - 
https://learning.acm.org/techtalks/recommendersystems