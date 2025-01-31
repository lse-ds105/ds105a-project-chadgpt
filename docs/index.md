# DS105A-project-chadgpt 😎😎😎😎

## 📋Team Members

-   Zicheng Liu (zcliu35) \| BSc in Economics
-   Yuyao Bai (yuyaobai) \| BSc in Economics
-   Clarence Quek (kurarensu77) \| BSc in Economics
-   Yi Song (songgyi) \| BSc in Economics

## 🍗 Spicing Up Data: An Analytical Feast on r/recipe

As a student facing the challenges of independent living at LSE, have you experimented with any recipes shared on r/recipes? Better yet, have you actively added your own culinary creations to this subreddit? If you're navigating through the multitude of recipes available and seeking your ultimate go-to meal for tight budgets and busy schedules, look no further!

Having experienced the struggles firsthand, we're here to guide you in making informed decisions. Discover the most highly praised recipes on r/recipes and identify the ones with optimal nutritional value to create the ultimate go-to meals for your student journey. Whether you've been through it or are currently navigating it, we're here to assist you in choosing recipes that not only meet your taste preferences but also provide the essential nutrients needed for the best struggle meals ever!

### Our Data Source

-   [r/recipes](https://www.reddit.com/r/recipes/)
-   [BBC Good Food](https://www.bbcgoodfood.com/)

### Motivation

Our project's origin story began on a Thursday night as the four of us gathered to brainstorm ideas before our DS105A class. Hungry and in need of a break, we ventured to a nearby fried chicken shop known for its delectable spicy sauce. Curious about its secret ingredients, we turned to Reddit for answers. To our delight, we stumbled upon a well-organized subreddit dedicated to culinary exploration. Inspired by our discovery, we decided to explore our findings on r/recipes and share with our fellow coursemates.

## 📋PROJECT Roadmap

![Plot: Project Roadmap!](project_chadgpt_roadmap.png)

### ⚙️Project Hypothesis

We suggest a hypothesis that implies **popular food**, as evidenced by a **high upvote ratio**, may demonstrate **reduced nutritional content**. We aim to investigate and substantiate or refute this assertion through further exploration and analysis.

## 📋General Outline

### 📖Part 1 (Initial Scraping and Cleaning)

-   We started off with r/recipes, where we used the Reddit API to get the data that we want (title of post, date and time created, number of upvotes, upvote ratio, number of comments, url)
-   Example of raw data frame obtained from Reddit:
    -   <iframe src="posts.html" style="width: 100%; height: 400px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 2px 2px 5px #888;">

        </iframe>

        Full data frame shape: 2065 x 113

    -   We received around **2065** recipes from the Reddit API, containing basic details like links, upvote ratios, post flairs, and upvote counts. The dataframe is raw and needs cleaning, with redundant columns to be removed
-   Prior to data cleaning, we accessed the original poster's comment, a crucial step as it contains the OP's recipe and ingredients list for us to test our hypothesis.
-   Observation: We selected this subreddit under the assumption that its posts maintain a well-structured format regulated by moderators. However, some posts required data cleaning due to improper formatting or deletion.\
    Data Cleaning Steps:
    -   1️⃣ Filtering out posts with **non-English titles** was achieved through a custom function called "Chadtools", leveraging the Langid package.
    -   2️⃣ **Conversion** of data types to more efficient formats (such as from int64 to int16) was performed to enhance computational efficiency.
    -   3️⃣ Posts dated before August 31, 2020, were excluded. This decision was influenced by r/recipes' implementation of **stricter regulations from that date onwards**, resulting in more consistently formatted posts.
-   Example of the filtered data set 
    -   <iframe src="df_filtered.html" style="width: 100%; height: 400px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 2px 2px 5px #888;">

        </iframe>

        Full data frame shape: 998 x 12

    -   In this dataset, we have most of the information we require for initial analysis of the posts.🤩 We will move on to ingredient and recipe analysis in conjunction with data from BBC Good Food in Part 2.

### Part 1 📊 Initial Analysis of Reddit Data

We analysed data from Reddit and observed some trends on posts with different flairs!  
![Plot: Dessert Flair is the most popular!](plot_top_10_percent_upvote_ratio.jpg)   
- Remarkably, within the **top 10%** of posts ranked by **upvote ratio**, those labeled with the **"dessert"**🍦 flair exhibit the highest frequency. Notably, this occurrence surpasses the **second-highest**, **"poultry"**🍗 by more than half. It suggests a **strong inclination among Reddit users towards favoring dessert-related posts.** Our theory is that dessert posts fulfil a wider range of dietary restrictions and thus appeal to a larger audience base.   

![Plot: All flairs are skewed to the left!](plot_all_upvote_ratio.jpg)   
- Furthermore, an overarching observation across all posts reveals a **conspicuous left skew** (longer left-tail) in the distribution of upvote ratios. This skew suggests that a significant majority of posts tend to **approach a ratio of 1**. Such a pattern implies the existence of a community within this subreddit that is supportive and benevolent. Notably, this trend persists across individual flair categories in Reddit posts.

### 📖Part 2 (Further Scraping and Cleaning)

#### ⚙️Linking r/recipes and BBC Good Food

Approach:   
1. Obtain recipe titles and their respective nutritional data (calories, fat, fibre, sugar, protein etc) from BBC Good Food   
- Sent a GET request to https://www.bbcgoodfood.com/search?q=   
- Webscraping using a mixture of CSS and XPath selectors   
- Example of filtered nutritional information and user ratings scraped   
- <iframe src="bbc_data.html" style="width: 100%; height: 250px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 2px 2px 5px #888"></iframe>   
    - Full data frame shape: 10011 x 11

2.  **Calculating cosine similarity score and merging columns based on the maximum similarity**  

-   Employed a NLP model - `sklearn's SentenceTransformers` - to convert each recipe title into an embedding
-   Calculated the cosine similarity score between each pair of embeddings of Reddit and BBC Good Food recipe titles
    -   The closer the cosine similarity score is to 1, the more similar the recipes titles
-   Only retain the pairs where the cosine similarity score is above the threshold that we set (0.75), and these are considered matches
    -   If there are multiple matches of different BBC Good Food titles to the same Reddit recipe title, we only keep the match with the highest cosine similarity score
-   This approach yields 467 recipes with matches, a sufficient number for us to conduct further analysis
-   Upon finding a match, we integrate additional details from the BBC Good Food dataset into our existing Reddit dataset
-   Example of merged dataframe between BBC Good Food and r/recipes
    -   <iframe src="merged_data_for_analysis" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 2px 2px 5px #888;">

        </iframe>

        -   Full data frame shape: 467 x 20

#### Extracting Cuisine and Ingredients

- Used `GPT-3.5-turbo` via the OpenAI API to infer the cuisine and extract a list of basic ingredients for each recipe.

- Prompted GPT to identify the cuisine of the recipe and extract the ingredients, given a string containing the recipe.

- We decreased the temperature to ensure that GPT followed our prompts more closely and didn't get too "creative" with the answers

- We specified a seed value to ensure that the results were reproducible

### Part 2A 📊 Analysis of Merged Reddit and BBC Good Food Data

<iframe src="interactive_plot.html" style="width:100%; height:700px; border:none;">

</iframe>

The above plot shows that there is no clear relationship between the popularity of a recipe (using Reddit upvote ratio as a proxy) and the healthiness of a recipe (using calorie count as a proxy)-- this means that our initial hypothesis is incorrect! By choosing select flairs on the legend, we see that this lack of correlation holds regardless of the category of food that the recipe falls under. One possible reason for this lack of correlation is that the motivation behind upvoting may extend beyond the perceived healthiness of a recipe. Visual appeal, creativity, the story behind the recipe, or a desire to support the OP (Original Poster) can all influence upvotes more than nutritional content.  

We also made another interesting observation that many posts have exactly the same upvote ratio (down to 10 decimal places). The upvote ratio was also always close to a whole number (e.g. 0.9501963125). This could be due to normalisation or rounding errors in Reddit's processing.
  
Follow the link on each point (using **cmd+click/ ctrl+click**) to find a recipe that is both well-received and meets your nutritional goals!   
  

<iframe src="upvote_ratio_vs_bbcgf_rating" style="width:100%; height:700px; border:none;">

</iframe>

We observe a strong association between higher Reddit upvote ratios and higher BBC Good Food ratings. One possible reason is that some recipes may have a universal appeal due to their taste or prevalance across many cuisines. These recipes naturally attract positive attention and higher ratings on platforms like BBC Good Food and similarly receive more upvotes on Reddit.

However, there are some interesting outliers.  
1. British Baked Cabbage with Cheese Casserole 
- This is the post with the lowest upvote ratio on Reddit, yet it has a relatively high BBC Good Food rating. 
- When we follow the link of this point on the plot and observe the Reddit post and comments for this recipe, we can tell that this post is likely a troll post. 
- However, the cosine similarity test is purely based on the titles (without contextual information from the comments to signal that this is a troll post), so the corresponding nutrition data and user ratings from BBC Good Food will be inaccurate.

2.  Easter Egg Blondies
-   This post has a high Reddit upvote ratio, yet it has the lowest BBC Good Food rating.
-   Investigating the corresponding [post](https://www.bbcgoodfood.com/recipes/easter-egg-blondies) on BBC Good Food, we can tell from the comments that the recipe is flawed, both in its procedure and quantities of ingredients, and does not produce a tasty dish!
-   This exposes an imperfection in our approach -- ingredients and cooking procedure have a huge impact on how well-received a recipe is, despite the Reddit and BBC Good Food recipe titles being highly similar.

### Part 2B 📊 Analysis of extracted cuisine and ingredients
We obtained the top 10 most common cuisines featured on Reddit and for the remaining cuisines, grouped them together as 'other'. We also collected the top 10 most common ingredients used and plotted these two variables as a stacked bar chart.  
![Plot: linking most common ingredients and cuisines](top_10_ingredients_cuisine.jpg)  
- A large proportion of the top 10 most common ingredients are seasonings and flavourings, which is to be expected as almost all recipes will require these. 
- Some interesting findings:  
    - Olive oil and white onions feature prominently in Italian cuisine 
    - Mexican and Indian cuisines rarely use eggs in their recipes 
    - Chinese cuisine rarely contain butter in their recipes  

We also calculated the average nutritional data (calories, carbohydates, fat, salt, sugar, saturates) for each of the top 10 cuisines. After obtaining benchmark values for these data from BBC Good Food and NHS, we visualise this information in radar charts for easy comparison. We have excluded the protein and fibre values from the radar charts, as more protein and fibre are generally considered healthier unlike the other nutritional indicators, so including all the nutrition data would complicate our radar chart.

- In the charts below, the values for each nutrient have been min-max normalised, so that the values lie between 0 and 10. 0 indicates the lowest amoutn of each nutrient relative to all the cuisines, and 10 indicates the highest.

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Image Grid</title>
<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 10px;
  }
  .grid-item {
    width: 100%;
    height: auto;
  }
</style>
</head>
<body>
<div class="grid-container">
  <div class="grid-item"><img src="./plots/radar_plot_American.png" alt="American"></div>
  <div class="grid-item"><img src="./plots/radar_plot_British.png" alt="British"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Chinese.png" alt="Chinese"></div>
  <div class="grid-item"><img src="./plots/radar_plot_French.png" alt="French"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Greek.png" alt="Greek"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Indian.png" alt="Indian"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Italian.png" alt="Italian"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Japanese.png" alt="Japanese"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Mexican.png" alt="Mexican"></div>
  <div class="grid-item"><img src="./plots/radar_plot_Thai.png" alt="Thai"></div>
</div>
</body>  
</html>

- One very intriguing finding is that Chinese cuisine is (on average) the healthiest cuisine out of the top 10 most popular ones. For all 6 indicators, values lie below the threshold significantly (except salt). Indian, Japanese and Thai cuisines also fare pretty well, with most indicators lying below the threshold. For the more health-conscious students at LSE, Chinese cuisine may be the way to go!
- On the other hand, American, British and French cuisine stand out with higher sugar profiles, which might reflect the prevalence of sweetened foods and beverages in these diets, suggesting that these cuisines are more unhealthy.

For all our fellow LSE students out there, when you move into your new accommodation next year, these 10 most-used ingredients are your move-in kitchen staples for you to become a meal prep monster!  
<iframe src="ingredient_frequency.html" style="width: 200px; height: 350px; border:none;"></iframe>   

### 📖Overall Conclusion
We observe that our initial hypothesis regarding the correlation between the healthiness of a recipe and its popularity was incorrect. On hindsight, our hypothesis was perhaps restricted in its perspective, as there are after all many other variables that affect the popularity of a post, such as the aesthetics or story behind the post, or even the algorithm behind the post. Nevertheless, in our culinary exploration, we still managed to make a number of interesting findings as documented above which we did not expect. 

We recognize that our project and approach has its limitations. For example, while we have linked recipes from r/recipes and BBC Good Food using their titles as a basis for comparison, there is a chance that recipes bearing the same name may actually vary significantly in preparation and cooking technique. Such discrepancies could result in end products with different nutritional values, which our title-based approach might not capture. We are aware that fully accounting for this is quite a formidable task at present, yet we are confident in the robustness of our current analysis.

### 📖Challenges

#### ❎ 1: Reddit API Limits

-   Reddit's API limits a search query to 250 results only
    -   To overcome this challenge, we iterated over a list of flair names for a specific subreddit and combined post data from each flair by extending a list!

#### ❎ 2:Extracting Reddit recipes and ingredients

-   Extracting the OP's comment containing the actual recipe posed a challenge. While we could use one of the Reddit API Keys to target all OP's comments, we faced difficulties isolating the specific comment with the desired recipe.
    -   To overcome this challenge, we made an assumption: The OP's recipe comment will be LONGER all other comments by the OP. This proved to be very powerful as we are able to target the OP's original comment with ingredients and instructions for all the posts on r/recipes, simply by isolating the *longest* comment. 

#### ❎ 3: Analysing Reddit recipes and ingredients

-   Analysing the ingredient lists provided by the OP on Reddit was difficult, as there was a lot of variance and the formatting of ingredient lists still differed despite the subreddit's stricter regulations on the format of posts. The ingredients were often not well-formatted, making it difficult to identify the exact ingredient using NLP. For instance, it was challenging to get Spacy or Regex to identify that the main ingredient in the line `1 clove of garlic, minced` was `garlic`. To overcome this challenge, we decided to use GPT 3.5, as it is a very well-trained model that proved to be much better at identifying the primary ingredients when a high variation in formatting is present.

## 📋Appendix

### 🔥🔥🔥🔥Contributions

-   Zicheng Liu (zcliu35)
    - Radar charts, scraping Reddit data, cleaning data
-   Yuyao Bai (yuyaobai)
    -   Cosine similarity test to link Reddit and BBC GoodFood, interactive plots, scraping BBC data
-   Clarence Quek (kurarensu77)
    -   Scraped OP's comment and did plots, website, cleaning data
-   Yi Song (songgyi)
    -   Langid to remove non-English posts, website

### 🔎References
- [BBC Good Food Guide to Healthy Eating](https://www.bbcgoodfood.com/howto/guide/good-food-guide-healthy-eating)
- [NHS Eatwell Guide](https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/the-eatwell-guide/)
