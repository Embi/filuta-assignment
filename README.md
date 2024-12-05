# Filuta Assignment
This repository presents a possible solution to a simple car recommender system
design. The solution primarily focuses on back-end software/infrastructure engineering
aspects of the problem. Front-end layer is completely omitted and datascience
solution is rather naive (with a lot of assumptions pulled out of my ass).
Tho it was necessary to pick some datascience solution as it dictates some parts
of the presented back-end tech stack (like a database and event handling...).

The solution presented here consists of:

* [Naive recommender design](#naive-recommender)
* [Architecture](#architecture)
* [Prototype](#prototype)

# Naive recommender
As mentioned in the introduction, in my opinion, some datascience solution had
to be picked to be able to design the back-end stack. 

After a quick research, I essentially ruled out using any complex ML solutions
(since I don't have experience nor intuition in this domain and thus it would be too
time consuming) and narrowed it down to two possible solution (ideally a hybrid of both)
and ordered them based on complexity:

1) Content-based filtering
2) Collaborative filtering

Both solutions seems to boil down to computing some "preference" vector for the user
(either based on some real feature set, in case of content-based filtering,
or latent feature set, in case of collaborative filtering) and representing
each car listing by a feature vector (again either based on real features
or latent ones). Then the recommendations for the user are obtained by finding
nearest car listing neighbours to the users "preference" vectors.

So a high level solution could look something like this
![recommender](diagrams/recommender.png "Recommender")

# Architecture 
This chapter presents possible software stack and interactions between various stack
components. 

Product layer:
![recommender](diagrams/product-layer.png "SW Stack")

Monitoring Layer:
![monitoring](diagrams/monitoring-layer.png "SW Stack")

# Prototype
#TODO
