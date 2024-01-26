# DS105A-project-chadgpt
Project Chadgpt


## 📋Team Members 
- Zicheng Liu (zcliu35) | BSc in Economics
- Yuyao Bai (yuyaobai) | BSc in Economics
- Clarence Quek (kurarensu77) | BSc in Economics
- Yi Song (songgyi) | BSc in Economics


## 🍗 Spicing Up Data: An Analytical Feast on r/recipe
As a student facing the challenges of independent living at LSE, have you experimented with any recipes shared on r/recipe? Better yet, have you actively added your own culinary creations to this subreddit? If you're navigating through the multitude of recipes available and seeking your ultimate go-to meal for tight budgets and busy schedules, look no further!

Having experienced the struggles firsthand, we're here to guide you in making informed decisions. Discover the most highly praised recipes on r/recipe and identify the ones with optimal nutritional value to create the ultimate go-to meals for your student journey. Whether you've been through it or are currently navigating it, we're here to assist you in choosing recipes that not only meet your taste preferences but also provide the essential nutrients needed for the best struggle meals ever!

### Our Data Source
- [r/recipe](https://www.reddit.com/r/recipes/)
- [BBC Good Food](https://www.bbcgoodfood.com/)

## 📋PROJECT Roadmap
to insert roadmap here
(Also, insert explanation of Roadmap)

## 📋General Outline
### 📖Part 1 
- We started off with r/recipe, where we used reddit api to get the data that we wanted (title of post, date and time created, number of upvotes, upvote ratio, number of comments, url)
- Cleaned the data (such as filtering out non english...changing data type...)


### Part 1 📊Analysis
We analysed data from reddit and observed some trend on posts with different flairs!
- insert pic (plot_top_10_percent.jpg)
    - Remarkably, within the top 10% of posts ranked by upvote ratio, those labeled with the "dessert" flair exhibit the highest frequency. Notably, this occurrence surpasses the second-highest, "poultry," by more than half. It suggests a strong inclination among Reddit users towards favoring dessert-related posts.
- insert pic (plot_all.jpg)
    - Additionally, across all posts, there is a notable rightward skew in the distribution of upvote ratios, indicating that a majority of posts have ratios approaching 1. This pattern suggests a community of users on this subreddit who are notably supportive and benevolent.

### 📖Part 2 
(to describe technical steps without too many details)
- We then got the information from BBC good food
- Ran a Cosine similarity test to match recipes


### Part 2 📊Analysis
- Present findings

### 📖Overall Conclusion

### 📖Challenges
#### ❎Challenge 1
- Reddit's API limits a search query to 250 results only
    - To overcome this challenge, we iterated over a list of flair names for a specific subreddit and combining post data from each flair by extending a list!
#### ❎Challenge 2
- Extracting the OP's comment containing the actual recipe was challenging because while we can use one of the Reddit API Keys to target all OP's comments, we faced problems isolating the commet with recipe which we wanted.
    - To overcome this challenge, we made an assumption: The OP's comment we want will be LONGER 
    all other comments by the OP. Through this, we are able to target the OP's original comment with ingredients and instructions.
#### ❎Challenge 3
- Excluding posts in languages other than English posed challenges, as the utilization of Langid to identify non-English titles, even with a low confidence level (indicating a less stringent removal of titles), resulted in a narrowed dataframe to only 28 posts. This occurred despite the presence of a few non-English posts in the dataset.
    - We created a custom function (chadtools_is_english) to get just english posts. We used .apply() to apply our function to each element in the 'title' column. 
    - (Insert screenshot)
    - This function checks if the text is in English using the spaCy language model (nlp)
## 📋Appendix
### Contributions
- Zicheng Liu (zcliu35) 
    - Hard carried
- Yuyao Bai (yuyaobai)
    - Hard carried
- Clarence Quek (kurarensu77) 
    - got carried
- Yi Song (songgyi) 
    - got carried.....


