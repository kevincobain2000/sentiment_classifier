Test Run
========

Negative Review 
----------------

This is quite possibly the worst movie ever made. Even my 4 year old hated it and wanted to leave. I was using it as an excuse to nap in air-conditioning. Alas, it was so bad that my daughter insisted we leave. Not really a surprise for a Steven Paul film, but I’m saddened that Jon Voight’s career has fallen so low...and Scott Baio??? ARGH! Believe me, I’ve had to sit through some bad kid flix, but this one is an all time loser. There is a woman with very large lips (Vanessa Angel) who almost makes it bearable, just for the pure fascination of watching whether or not they will explode. However, my suggestion would be that all prints of this film be sent to President Bush so he can see how harmful his education budget cuts have been.

**Results**
::

  bash$ senti_classifier -c reviews 
  loading pickle........... 
  loading pickle successful 
  Training Bag Of Words........... 
  Training Bag Of Words successful 

  This is quite possibly the worst movie e          ...   positive= 0.0       negative= 0.875 
  Even my 4 year old hated it and wanted t          ...   positive= 0.375     negative= 0.25 
  I was using it as an excuse to nap in ai          ...   positive= 0.25      negative= 0.375 
  Alas, it was so bad that my daughter ins          ...   positive= 0.0       negative= 0.75 
  Not really a surprise for a Steven Paul           ...   positive= 0.25      negative= 0.25 
                                                    ...   positive= 0         negative= 0 
                                                    ...   positive= 0         negative= 0 
  and Scott Baio??? ARGH! Believe me, I’ve          ...   positive= 0.0       negative= 1.125 
  There is a woman with very large lips (V          ...   positive= 1.25      negative= 0.125 
  However, my suggestion would be that all          ...   positive= 0.375     negative= 0.375 
                                                    ...   positive= 0         negative= 0 
                                                          ----------------------------------- 
                                                    TOTAL POSITIVE= 2.5       NEGATIVE= 4.125 
  reviews is NEGATIVE with score 4.125 

Positive review
---------------

As for the spectacle of the battle and showdowns, while not at the scale of Lord of the Rings, I honestly cant think how it could have been done better as the film makers have intertwined heart stopping action with dramatic progressions in the narrative. Its actually more visceral and dynamic than the rather smaller scale battle of the brilliant novels (not to take anything away from Rowling’s writing).
Do I have any gripes? Yes I do. Although I applaud Steve Kloves for a difficult screenplay adaption...I think he could still have done better at explaining some odd anomalies that only readers of the book will understand. This might annoy you if you haven’t read the books. But its a small gripe because what we get is delightful.
What an amazing achievement to faithfully bring Rowling’s epic saga to the big screen with the same cast and largely the same crew, maintaining the brilliant quality right to the end. 

**Results**
::

  bash$ senti_classifier -c reviews 
  loading pickle........... 
  loading pickle successful 
  Training Bag Of Words........... 
  Training Bag Of Words successful 

  As for the spectacle of the battle and s          ...   positive= 1.0       negative= 0.5 
  Its actually more visceral and dynamic t          ...   positive= 2.0       negative= 0.0 
                                                    ...   positive= 0         negative= 0 
  Do I have any gripes? Yes I do                    ...   positive= 0         negative= 0.5 
  Although I applaud Steve Kloves for a di          ...   positive= 0.0       negative= 0.0 
                                                    ...   positive= 0         negative= 0 
                                                    ...   positive= 0         negative= 0 
  I think he could still have done better           ...   positive= 0.875     negative= 0.25 
  This might annoy you if you haven’t read          ...   positive= 0.0       negative= 0.5 
  But its a small gripe because what we ge          ...   positive= 0.75      negative= 0.125 
                                                    ...   positive= 0         negative= 0 
  What an amazing achievement to faithfull          ...   positive= 1.875     negative= 0.0 
                                                    ...   positive= 0         negative= 0 
                                                          ----------------------------------- 
                                                    TOTAL POSITIVE= 6.5       NEGATIVE= 1.875 
  reviews is POSITIVE with score 6.5 

