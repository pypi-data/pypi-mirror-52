from cmdline_printer import ArticlePrinter
from analyzer import Article


########## Following will be removed from the Final code ##############

editorial_1_july = "/Users/waqas/code/homer/experiment/newspapers/editorial_1_july_19_br.txt"
editorial_2_july = "/Users/waqas/code/homer/experiment/newspapers/editorial_2nd_july_19.txt"
editorial_29_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_29th_july_br.txt"
editorial_25_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_25_br.txt"
editorial_26_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_26_br.txt"
editorial_28_jne = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_28_br.txt"


oped_9_feb_hafiz_pasha = "/Users/waqas/code/homer/experiment/newspapers/more_stagflation_9_feb_2019_br_hafiz_pasha"
oped_2_july_hafiz_pasha = "/Users/waqas/code/homer/experiment/newspapers/stab_effort_2_july_19_hafiz_pasha_br.txt"
oped_1_july_anjum = "/Users/waqas/code/homer/experiment/newspapers/tax_man_anjum_ibrahim_1_july_19_br.txt"
oped_1_july_andeel = "/Users/waqas/code/homer/experiment/newspapers/changing_perception_andeel_1_july_19_br.txt"

oped_dawn_5_july_sakib = '/Users/waqas/code/homer/experiment/newspapers/dawn_oped_sakib_sherani_5_july.txt'
oped_dawn_5_july_jihad_azour = '/Users/waqas/code/homer/experiment/newspapers/dawn_oped_jihad_azour_5_july.txt'
shabaz_4_july = '/Users/waqas/code/homer/experiment/newspapers/shabaz_july4_ecc_rejects.txt'

# econ survey
fiscal_dev = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/fiscal_development.txt'
inflation = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/inflation.txt'
manufacturing_and_mining = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/manufacturing_and_mining.txt'
money_and_credit = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/money_and_credit.txt'
overview_of_econ = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/overview_of_economy.txt'
oped = "/Users/waqas/code/homer/experiment/oped.txt"
roadmap = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/roadmap_for_stability_and_growth_mof.txt'
encoding = '/Users/waqas/code/homer/experiment/encoding/CDS.txt'
article = ArticlePrinter(Article('', '', open(oped).read()))
# article = Article('name', 'author', open('/Users/waqas/PycharmProjects/sense_of_style/experiment/economic_survey_pk_2018_19/overview_of_economy.txt').read())
article.print_article_stats()
# # print(article.words_with_most_syllables())
article.print_paragraph_stats()
