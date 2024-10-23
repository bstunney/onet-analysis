# Ben Tunney

# Packages
import pandas as pd
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt

# Methods
def get_indices(list_of_lists):

    # Find keys that occur in all lists
    common_keys = set()
    for combination in combinations(list_of_lists, 4):
        common_keys |= set.intersection(*map(set, combination))

    return common_keys

def top_work_activities(unimportant_top_n_items, important_top_n_items):

    # Extract labels and sizes from the counter dictionary
    labels = [val[0] for val in important_top_n_items]
    sizes = [val[1] for val in important_top_n_items]

    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set2.colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Top 5 Most Important Work Activities for Analytical Roles')
    plt.show()

    # Extract labels and sizes from the counter dictionary
    labels = [val[0] for val in unimportant_top_n_items]
    sizes = [val[1] for val in unimportant_top_n_items]

    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel2.colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Top 5 Least Important Work Activities for Analytical Roles')
    plt.show()

def top_tech_skills(top_analytical_tech_counts, top_nonanalytical_tech_counts):

    # Extract labels and sizes from the counter dictionary
    labels = [val[0] for val in top_analytical_tech_counts]
    sizes = [val[1] for val in top_analytical_tech_counts]

    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors = plt.cm.Set2.colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Top 5 Technical Skills for Analytical Roles')
    plt.show()

    # Extract labels and sizes from the counter dictionary
    labels = [val[0] for val in top_nonanalytical_tech_counts]
    sizes = [val[1] for val in top_nonanalytical_tech_counts]

    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel2.colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Top 5 Technical Skills for Non-Analytical Roles')
    plt.show()

def main():

    """""""""""""""""""""""""""
    # ANALYTICAL WORK INDEX
    """""""""""""""""""""""""""

    # Skills Dataset
    skillsdf = pd.read_csv("db_28_2_text/Skills.txt", sep='\t')

    # skills requiring analytical experience or thinking
    skills_lst = ['Technology Design', 'Systems Evaluation', 'Systems Analysis',
                  'Mathematics', 'Programming', 'Science']
    skills_keys = skillsdf[skillsdf["Element Name"].isin(skills_lst)]["O*NET-SOC Code"]

    # Knowledge Dataset
    knowledgedf = pd.read_csv("db_28_2_text/Knowledge.txt", sep='\t')

    # knowledge relating to fields requiring analytical thinking
    # largely following STEM guidelines, assumption that stem labor fields require a problem solving analytical component
    # along with technical skills that require analytical thinking EX: programming, life science computation, etc
    knowledge_lst = ['Biology', 'Engineering and Technology', 'Mathematics', 'Chemistry', 'Physics',
                     'Economics and Accounting', 'Computers and Electronics','Medicine and Dentistry','Psychology']
    knowledge_keys = knowledgedf[knowledgedf["Element Name"].isin(knowledge_lst)]["O*NET-SOC Code"]

    # Abilities Dataset
    abilitiesdf = pd.read_csv("db_28_2_text/Abilities.txt", sep='\t')

    # Abilities relating to fields requiring analytical thinking
    # Largely physical skills in this list, but chose skills that are essential to analytical thinking
    abilities_lst = ['Mathematical Reasoning','Number Facility']
    abilities_keys = abilitiesdf[abilitiesdf["Element Name"].isin(abilities_lst)]["O*NET-SOC Code"]

    # Tech Skills Dataset
    techdf = pd.read_csv("db_28_2_text/Technology Skills.txt", sep='\t')

    # Went through tech skills and chose keywords that corresponded to analytical tech skills
    tech_words = ["data", "network", "program", "cloud", "development", "medical", "accounting", "CAD"]
    techskills_lst = [title for title in set(techdf["Commodity Title"]) if any(word.lower() in title.lower() for word in tech_words)]
    techskills_keys = techdf[techdf["Commodity Title"].isin(techskills_lst)]["O*NET-SOC Code"]

    # Sample lists of primary keys
    lists = [list(skills_keys),list(knowledge_keys),list(abilities_keys), list(techskills_keys)]
    common_keys = get_indices(lists)

    # Print data subset size
    odf = pd.read_csv("db_28_2_text/Occupation Data.txt", sep='\t')
    print()
    print("Number of all jobs:",len(set(odf["O*NET-SOC Code"])))
    analytical_df = odf[odf["O*NET-SOC Code"].isin(common_keys)]
    print("Number of Analytical jobs:", len(set(analytical_df["O*NET-SOC Code"])))
    print()

    """"""""""""""""""""""""""""""""""""
    """ TECHNOLOGY SKILLS DATA ANALYSIS  """
    """"""""""""""""""""""""""""""""""""

    # Get analytical subset of technical skills dataset
    analyticaltechskills = techdf[techdf["O*NET-SOC Code"].isin(common_keys)]

    # Count occurrences of each item
    analytical_tech_counts = Counter(list(analyticaltechskills["Commodity Title"]))

    # Get the top N occurring items
    top_analytical_tech_counts = analytical_tech_counts.most_common(5)
    print("Top tech skills for analytical roles:", analytical_tech_counts.most_common(15))

    # Get non-analytical subset of technical skills dataset
    nonanalyticaltechskills = techdf[~techdf["O*NET-SOC Code"].isin(common_keys)]
    # Count occurrences of each item
    nonanalytical_tech_counts = Counter(list(nonanalyticaltechskills["Commodity Title"]))

    # Get the top N occurring items
    top_nonanalytical_tech_counts = nonanalytical_tech_counts.most_common(5)
    print("Top tech skills for nonanalytical roles:", nonanalytical_tech_counts.most_common(15))
    print()

    # Make Technical skills visualizations
    top_tech_skills(top_analytical_tech_counts, top_nonanalytical_tech_counts)

    """"""""""""""""""""""""""""""""""""
    """ WORK ACTIVITY DATA ANALYSIS  """
    """"""""""""""""""""""""""""""""""""

    # Get work activities of analytical roles
    fullworkdf = pd.read_csv("db_28_2_text/Work Activities.txt", sep='\t')
    workdf = fullworkdf[fullworkdf["O*NET-SOC Code"].isin(common_keys)]
    workdf["Data Value"].apply(lambda x: float(x))

    # get important work activities
    importantwork = workdf[(workdf["Scale ID"] == "IM") & (workdf["Data Value"] > 4)]

    # Count occurrences of each item
    important_item_counts = Counter(list(importantwork["Element Name"]))

    # Get the top N occurring items
    important_top_n_items = important_item_counts.most_common(5)
    print("Important work activities for analytical roles:", important_item_counts.most_common(15))

    # get unimportant work activities
    unimportantwork = workdf[(workdf["Scale ID"] == "IM") & (workdf["Data Value"] < 1.5)]

    # Count occurrences of each item
    unimportant_item_counts = Counter(list(unimportantwork["Element Name"]))

    # Get the top N occurring items
    unimportant_top_n_items = unimportant_item_counts.most_common(5)
    print("Unimportant work activities for analytical roles:", unimportant_item_counts.most_common(15))

if __name__ == "__main__":
    main()