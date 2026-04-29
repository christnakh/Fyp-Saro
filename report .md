

Final Year Project Proposal
Data-Driven Prediction of Material Waste in Construction Projects Using Machine Learning









Advisors:
(Department of Civil and Environmental Engineering)
	Dr. Mohamed-Asem Abdul Malak
	Dr. Farah Demachkieh

	
By:
•	Lucas Chebly	202305338
•	Saro Meghdessian	202309358
•	Shahan Nadjarian	202304615
•	Jad Raad	202309924
		
Table of Contents
List of Figures	iii
List of Tables	iii
	Concept Summary	1
	Second Semester: System Extension and Implementation	1
	Background and Project Objectives	2
	Problem Context	2
	Background Data and previous work	2
	Drivers of Steel Waste	3
	Algorithm Selection	5
	Significance of the Project	6
	Objectives	7
	Scope of Work and Methodology	8
	Scope of Work	8
	Methodology	9
	Approach	9
	Software/Tools	12
	Ethics & Safety	13
	Project Constraints	14
	Data Availability and Quality	14
	Time and Scope Limitations	14
	Interdisciplinary Knowledge Gap	14
	Implementation Plan and Schedule	15
	Project Resources and Budget	16
Acknowledgments	17
References	18
Appendix	21
	(Technical appendix: see TECHNICAL_APPENDIX_FULL.md in project root — for final PDF/print)	—

List of Figures

Figure 1. 2024 Steel Production Demand by Sector	2
Figure 2. Flow at Steel at Construction Site	3
Figure 3. Project Framework	9
Figure 4. Steel Waste Estimation - Web Interface Output	14
Figure 5. Steel Waste Prediction - Part of Web Interface Input	14
Figure 6. Implementation Plan	17

List of Tables
Table 1. Data Source and Format According to Type	11
Table 2. Data Generation Dictionary	12
Table 3. ML Performance Metrics for the Preliminary Dataset	13
Table 4. Total Cost Breakdown	18

 
	Concept Summary

In the Middle East, construction materials make up 50–60% of total project costs (Gao et al., 2024), yet most contractors continue relying on fixed waste allowances of 5–15% due to the absence of reliable, data-driven estimation tools (Ajayi et al., 2017). Steel reinforcement alone accounts for 3–8% waste (Widjaja et al., 2023), often caused by variations in site, management and design practices (Ren et al., 2023; Fu et al., 2025). Despite the financial and environmental impact of these inefficiencies, the region lacks a practical framework that links academic knowledge with real project data, presenting an opportunity for ways of better estimation.

This project develops a machine-learning framework tailored to Middle Eastern construction practices to improve steel waste prediction. The model estimates waste percentages using parameters from recent literature and site data, supported by a rigorously built synthetic dataset used to train and test multiple algorithms as a proof of concept. In the second semester, the team implemented the proposed system extension: the web application was rebuilt as a Flask-based decision-support tool with model explainability (SHAP or feature-importance fallback), prediction reliability indicators, integrated cost and CO₂ impact estimation, a JSON prediction API, and expanded documentation pages. Public cloud hosting remains an optional final step for demonstration and access. Ongoing work may still expand the dataset with additional variables and real project records as industry data becomes available. Once validated on wider data, the project delivers a practical framework for construction waste estimation, advancing data-driven waste prediction in the region.

	Second Semester: System Extension and Implementation

	Where to insert SECOND_SEMESTER_ADDENDUM.md in this report
	Put the addendum here in the main body—after the Concept Summary and before “Background and Project Objectives”—not at the end of the report after References or Appendix. The end of the document is only for items like TECHNICAL_APPENDIX_FULL.md and data listings. Your Table of Contents already lists “Second Semester: System Extension and Implementation” in this early position; keep it here and set the page number after you paste.

	What to copy from SECOND_SEMESTER_ADDENDUM.md
	Open the file SECOND_SEMESTER_ADDENDUM.md in the same project folder. Copy from the heading “## 1. Introduction and motivation” through the end of the file (through “## 13. Key code references …” and the closing italic note). Do not copy the first block titled “## How to use this document in the main report”—that part is instructions for authors only. When pasting into Word, convert “##” headings to your report’s heading levels (e.g. Level 1 / Level 2). If you keep working in Markdown, you may paste the same range directly under this note and delete these three instructional paragraphs for the final export.

	Short summary (until you paste the full addendum)
	The second semester implemented the extension proposal: Flask web app, SHAP or feature-importance explanations, prediction reliability (high/medium/low), cost and CO₂ from user-supplied steel mass, JSON API, and About/Features pages. Full narrative, architecture, formulas, limitations, and code references are in SECOND_SEMESTER_ADDENDUM.md sections 1–13.

	Background and Project Objectives
	Problem Context
Construction projects in the Middle East still rely on experience-based estimation for material waste, leading to inaccurate ordering. This project addresses that gap by using regional data and machine learning to predict waste based on project-specific factors, helping engineers, particularly in tendering, bidding, and estimating departments, better estimate steel requirements through a web interface where project parameters are entered and an estimated waste percentage is calculated along with CO2 reductions and cost savings. With limited data, the initial focus is on steel waste as a controlled proof of concept.
Steel reinforcement is a major cost component in reinforced concrete construction, accounting for 10–20% of structural costs (World Steel Association, 2022). Yet forecasting steel waste remains unadopted. Additionally, the steel industry generates about 7 percent of global energy-related CO₂ emissions (International Energy Agency, 2024). Construction accounts for roughly half of this footprint, reflecting its share of steel demand. In our case, additional emissions arise from transportation, cutting, etc. 





	Background Data and previous work

Reinforcement steel (rebar) waste stands out for its financial, given steel’s high procurement cost. Accurately predicting waste levels rather than relying on fixed allowances can significantly improve cost estimation and resource allocation (Gao et al., 2024; Hosny et al., 2023).
Through this model we plan to predict “Steel Waste Percentage”, which is planned to be the dependent variable in the model, it is defined as:
Steel Waste (%)=  (Ordered-Installed Theoretical)/(Installed Theoretical)  x 100

	Drivers of Steel Waste

The flow of steel is illustrated in Figure 1, where X denotes the total ordered quantity, W represents the wasted quantity, and X − W indicates the amount actually utilized or “consumed” in the construction project.
Steel is a huge contributor to industrial emissions, while its use in reinforced concrete construction increases the pressure on the industry to decrease material wastes (World Steel Association, 2022; International Energy Agency, 2024). Construction waste continues to be one of the biggest waste streams across the globe. Early papers found that material waste in building projects is the result of design deficiencies, poor coordination, and weak site management practices (Bossink & Brouwers, 1996; Poon et al., 2004; Al-Hajj & Hamani, 2011; Tam et al., 2007). This identified that wasting is not an unavoidable by-product of construction but rather systematic and preventable waste.
This was followed by other studies pointing out that design and procurement play an upstream role in minimizing waste. Ajayi, Akinade et al. showed that waste is generated from poor detailing, fragmented procurement, and lack of supply-chain control. They, therefore, advocated "designing out" the wastes and optimizing the ordering strategies (Ajayi et al., 2015; Ajayi et al., 2017; Akinade et al., 2018). Other research about concrete and ready-mixed concrete waste also reiterated how poor planning and ordering policies strongly predict losses (Lim et al., 2018; Adams & Hobbs, 2023). These insights have framed rebar as a strategic material where targeted interventions may result in large benefits.

Rebar waste arises specifically from cutting losses, obsolete lengths after design changes, fabrication errors, and limited offcut reuse (Formoso et al., 2002; Ekanayake & Ofori, 2004). Case studies in Malaysia and other regions demonstrate that contract type, frequency of change orders, and quality of supervision are determining factors in total waste (Begum et al., 2009; Botchway et al., 2023). Socio-economic studies highlighted the significance of training and organizational culture in achieving steady waste reduction (Tafesse et al., 2022). Across contexts, reinforcement waste patterns correlate closely with design complexity, number of bar diameters and lengths, and handling/storage conditions.

Digitalization of construction improved rebar waste minimization, and allowed for more opportunities to do that. Quantity take-off based on BIM and digital inventory systems enhance material tracking and allow for more accurate fabrication of reinforcement steel. The integration of optimization algorithms with BIM provides great potential in reducing cutting waste (Akinade et al., 2018; Hosny et al., 2023). Enhanced computational approaches continue to emerge, including an improved PSO method for rebar engineering (Ren et al., 2023), multi-objective cutting-pattern optimization (Wang et al., 2024), a two-stage algorithm for beam reinforcement (Widjaja & Kim, 2023), BIM-based genetic algorithm optimization in pump station reinforcement (Fu et al., 2025), and Digital Twin–based layout optimization (Widjaja et al., 2025). Additional gains from cutting-pattern analysis were demonstrated in a related case (Putri et al., 2024). These cases have reliably shown how stock bar length policy, offcut reuse, and cutting optimization are measurable drivers of waste.

In parallel, predictive modeling for construction waste has grown. Multiple linear regression models for waste prediction were developed in residential construction projects (Elsadany & Elsharawy, 2025), while penalty-cost models quantified waste in contracting firms (Olawale & Ayodeji, 2022). Newer studies have shown the increasing importance of machine learning algorithms that classify and predict C&D waste based on attributes at the project level (Gao et al., 2024; Samal et al., 2025). These studies document that waste volumes are not generated randomly but are predictable from design, procurement, and management variables.

While there has been progress in predictive modeling, it is clear that most predictive models treat waste in construction as one aggregated category and do not focus on rebar as a target, despite well documented rebar waste driven by discrete, measurable parameters such as reinforcement ratios, stock length policies, supervision quality, revision frequency, and material control practices. Current practice still relies heavily on heuristic waste allowances that completely disregard project-specific drivers. The literature gap, therefore, lies in the lack of project-level, rebar-focused predictive models leveraging the expansive datasets made possible with BIM and modern site documentation. Addressing this gap enables proactive optimization of detailing, procurement, and fabrication, reducing both cost and embodied carbon in reinforced concrete construction.






	Algorithm Selection

The machine learning models selected for this study reflect the structure of steel-waste prediction, which involves mixed data types, engineering constraints, and nonlinear interactions among design, procurement, and site-management parameters (Samal et al., 2025). To establish a transparent baseline, four classical linear models—Linear Regression, Ridge Regression, Lasso Regression, and Elastic Net—were included because they capture linear relationships, offer interpretability, and are widely used in early predictive engineering studies (AIA, 2020; ASCE, 2020).

To model more complex interactions, the methodology incorporated Decision Tree, Random Forest, Extra Trees, AdaBoost, and Gradient Boosting, all of which have demonstrated strong performance in construction analytics and resource-efficiency research (WRAP, 2020; PMI, 2019). These tree-based ensemble models are well-suited for capturing nonlinear behavior and interaction effects that commonly arise in steel-handling practices, stock-length decisions, supervision quality, and cutting optimization workflows.

All models were trained under the same preprocessing pipeline, cross-validation procedure, and evaluation metrics to ensure fairness in comparison. The final selection prioritizes predictive accuracy, generalization capability, and suitability for deployment in a real-world construction engineering context.









	Significance of the Project

Numerous studies indicate that material waste rates vary significantly across projects, resulting in substantial overordering that could be mitigated through data-driven prediction. For instance, blockwork waste has been found to range between 10% and 23% (Adams & Hobbs, 2023), concrete waste between 1% and 13.2% (Lim et al., 2018), and rebar waste between 3% and 8% (Widjaja et al., 2023). Globally, steel manufacturing emits approximately 1.85 tonnes of CO₂ per tonne of steel (Hasanbeigi et al., 2022), meaning even a modest reduction in onsite waste can have meaningful climate benefits.
	
Predictive models have demonstrated strong capability in forecasting waste generation, enabling contractors to refine material-requirement estimates and avoid unnecessary over-ordering that ties up capital (Elsaadany & Elsharawy, 2025). By minimizing unexpected material-related expenses, contractors improve cash-flow stability and working-capital management, particularly when managing multiple ongoing projects. Furthermore, waste underestimation has been shown to impose significant “penalty costs” that erode profit margins in fixed-price settings, highlighting the importance of accurate forecasting for competitive bidding and financial risk mitigation (Olawale & Ayodeji, 2022). Together, these findings show that improved waste prediction has both environmental and economic consequences, enhancing capital efficiency, liquidity, profit protection and CO₂ reduction in construction operations. 
	Objectives

The objective of this project is to establish a practical and scalable framework for predicting material waste in construction. This will be achieved by first developing a functional web application that estimates steel waste based on project-specific site, management, and design parameters, testing whether integrating real site data with academic insights improves prediction accuracy.

	Data Collection & Analysis
	Build a dataset from synthetic or on-site data capturing steel waste drivers.
	Clean and process data to ensure accuracy and consistency for modeling.
	Map the parameters from literature review to the existing dataset, and identify ways of describing them from site data. Additionally, find ways to quantify the qualitative parameters.

	Machine Learning model development

	Develop and train ML models for steel waste prediction.
	Evaluate models to determine which algorithm offers the best balance of accuracy and computational efficiency, while satisfying the following baseline criteria:
	R² ≥ 0.60 on a hold-out project-level test set
	MAE ≤ 2.0% and RMSE ≤ 3.0%
	Interpret model results identifying the most influential waste factors.


	Design a user-friendly prediction web interface

	Build a final model, allowing estimators to predict accurate steel waste percentages.
	Develop a model, quantifying cost-saving potential and associated CO₂ reductions.

	Deliver a scalable, reproducible framework applicable to other materials
 
	Scope of Work and Methodology
	Scope of Work
The figure below outlines the project’s approach for the project, which will be applied to residential and commercial concrete projects only, excluding complex structures like bridges or rail systems due to limited data representativeness.
 
Figure 3. Project Framework
List of Tasks:

	Identify Parameters: Review literature to extract and align measurable steel waste drivers.
	Collect Data: Gather on-site or synthetic data ensuring relevance and coverage.
	Prepare Data: Clean, encode, and standardize all parameters for modeling.
	Generate Data: Generate synthetic data to supplement limited site records and support model training.
	Develop Models: Train ML algorithms to predict steel waste percentage.
	Model Selection & Evaluation: Assess model accuracy, determine the optimal model, and extract key waste drivers.
	Develop Web Application: Develop a simple web interface to run the model using user-entered project data, that produces the estimated steel waste percentage, along with the financial, environmental (CO₂ reduction) and social aspects of the project.
	Build Framework: Create a generalizable system linking literature and site data.


	Methodology
	Approach
An eight-step methodology will be adopted, beginning with parameter identification and concluding with the development of a functioning web-based program. The process will ultimately validate whether a framework that enables estimators to predict material waste percentages using a structured, data-driven approach is feasible.
	Parameter Identification
The methodology begins with parameter identification through an in-depth literature review, which will later be strengthened by expert input and industry data.
	Data Collection
Data collection will be carried out through project collaborators. So far, A.R. Hourie Enterprises has committed to providing multiple project datasets, which vary geographically throughout the middle east. This dataset will serve as the foundation for our analysis. We will attempt to supplement this with data from additional companies and projects to reduce biases and improve representativeness. 
	Data Preparation
Data was grouped according to type and processed to enable machine learning analysis, as shown in Table 1. Numerical features were standardized to maintain consistent scaling, while categorical parameters were label-encoded to ensure compatibility with the algorithms. Parameters were verified against quality-control rules to confirm that all values fell within realistic ranges. Additionally, data splitting was carried out at the project level, assigning entire projects exclusively to either the training or testing subsets. This approach prevents information leakage and ensures true generalization to unseen projects. These preprocessing steps were first applied to a synthetic dataset generated without real project input. The next stage will involve regenerating a synthetic dataset informed by actual project data. 

Table 1. Data Source and Format According to Type
Data Type	Description	Source	Format
Steel Usage Data	Quantity of reinforcement ordered, delivered, and installed	Site and procurement logs	Excel
Design Information	Reinforcement ratio, element types, BBS details	Structural design files	Word / Excel
Project Metadata	Project type, contract type, BIM level	Project management documentation	Word / Excel
Environmental Conditions	Weather parameters (temperature, humidity)	Meteorological API	Word / Excel

	Data Generation
The initial synthetic dataset was generated solely from literature, with a later version to incorporate real project data. Categorical variables were produced using industry-based probability distributions, followed by numerical variables generated through conditional logic reflecting engineering relationships and realistic correlations. Steel waste was computed using a research-derived function with fifteen factors and a 6.5% baseline plus stochastic noise. All outputs underwent validation checks to ensure coherence and reproducibility. The full code for this process is included in the appendix folder. A table visualizing the type of data, unit, range/categories, statistical distribution and QC check for each variable is attached in the appendix.
Table 2. Data Generation Dictionary
Variable Name	Unit	Range / Categories	Distribution	QC Check
Reinforcement ratio	kg/m³	80–250	Normal (μ≈160, σ≈25)	Value must be between 50–300
Unique number of reinforcement steel lengths	count	2–15	Discrete uniform	Must be integer ≥1
Stock length policy	–	{standard_12m,mixed_lengths,
custom_lengths}	Categorical	Must match allowed values
Cutting optimization usage	–	{none, partial, full}	Categorical	Must match allowed values
Bim integration level	–	0–3	Discrete	Integer 0–3
Monthly Design revisions	revisions/month	0–10	Poisson-like	Must be integer ≥0
Supervision Index	–	1–5	Uniform discrete	Integer in [1,5]
Material Control Index	–	1–3	Discrete	Integer in [1,3]
Storage Handling Index	–	1–5	Discrete	Integer in [1,5]
Offset reuse Policy	–	0=none,1=limited,2=systematic	Discrete	Integer in {0,1,2}
Monthly Change Orders	count/
month	0–8	Poisson-like	Must be integer ≥0
Contract Type	–	{lump_sum, remeasurement, cost_plus}	Categorical	Must match listed category
Lead Time Days	days	3–30	Right-skewed	Value must be >0
Order Frequency_ per Month	count	1–8	Discrete	Integer ≥1
Project Phase	–	{substructure, superstructure, finishing}	Categorical	Must match allowed category
Steel Waste Percentage	% of total steel	2–20%	Hybrid based on input factors	Must be between 0–30%





























	Model Development
Model development involved testing eight machine learning algorithms alongside a linear regression baseline. Each model was trained and evaluated using standard metrics to identify the most reliable predictor of steel waste.
	Model Evaluation and Selection
Once all models were trained, they were evaluated using a comprehensive set of performance metrics, including MAE, RMSE, R², MAPE, and cross-validation variance. The performance metrics were found to be in the range set in the objectives for all the models, with the Gradient Boosting algorithm performing the best, achieving the lowest MAE (0.73%), the lowest RMSE (0.92%), and the highest R² (0.93). This step will be repeated once the dataset is updated with real project data. The table below summarizes the results for the preliminary synthetic dataset.

Table 3. ML Performance Metrics for the Preliminary Dataset

Model	Test MAE (%)	Test RMSE (%)	Test R²	Test MAPE (%)	CV MAE (%)	CV R²	Overfitting
Gradient Boosting	0.73	0.92	0.93	10.88	0.77	0.92	0.06
Linear Regression	0.76	0.97	0.92	10.70	0.78	0.92	-0.00
Ridge Regression	0.76	0.97	0.92	10.70	0.78	0.92	-0.00
Elastic Net	0.81	1.01	0.92	12.81	0.82	0.91	-0.00
Lasso Regression	0.84	1.04	0.91	13.27	0.84	0.91	0.00
Extra Trees	0.96	1.20	0.88	15.23	1.03	0.86	0.11
Random Forest	1.01	1.25	0.87	16.43	1.08	0.85	0.09
AdaBoost	1.50	1.86	0.71	27.92	1.58	0.70	0.01
Decision Tree	1.56	1.99	0.67	22.24	1.63	0.63	0.29


	Development of Web Application
The Gradient Boosting model is served through a Flask web application (Jinja2 templates, Bootstrap, modular static assets). Engineers and estimators enter project parameters on a single prediction page and receive: (1) predicted steel waste percentage and a qualitative waste-performance band; (2) a prediction reliability badge and score; (3) cost and CO₂ metrics derived from total steel mass and literature-based default factors; (4) an explainability panel (SHAP when installed, otherwise feature importance) listing top drivers and direction of effect. JSON predictions are available via an API route for scripting or integration. Compared to the first-semester static HTML/CSS/JS prototype, this version centralizes logic in Python, keeps one trained artifact (`models/best_steel_waste_model.pkl`), and can auto-train if the artifact is missing and train/test CSVs are present. Screenshots should be refreshed to match the new layout (landing, predict, about, features). The application will be updated as real project data becomes available, ensuring the model and its correlations remain accurate and reflective of real-world conditions.
 
Figure 4. Steel Waste Estimation - Web Interface Output

 
Figure 5. Steel Waste Prediction - Part of Web Interface Input


	Framework Development
The developed framework for steel waste prediction will be designed to be scalable and adaptable to other construction materials. Once validated on steel, approach can be replicated with material-specific variables.
The process will involve identifying equivalent waste drivers for each material and redefining their measurable proxies based on both literature and site data. This approach will validate that more accurate waste estimation is practically feasible, demonstrating that predictive modeling can be applied effectively within real construction contexts. By maintaining a consistent methodology, the framework will enable future studies or industry partners to easily apply it across different material types. This ensures the research contributes not only to steel waste prediction but also to a broader, data-driven approach for improving material efficiency across construction projects.

	Software/Tools
The project will be carried out using personal laptops for data analysis and coding, supported by university computing resources when specialized software or higher processing power is required. Work will primarily use Python with libraries such as pandas, NumPy, and scikit-learn, alongside Jupyter Notebook and VS Code for development and testing. The deployed-style web layer uses Flask; explainability optionally uses the SHAP library (with graceful fallback). Excel will support data inspection. GitHub will manage version control and collaboration, and Microsoft Word and PowerPoint will be used for documentation and presentations.

	Ethics & Safety
All site data provided by Hourie Enterprises or other collaborators will be used only for academic purposes and anonymized to protect confidentiality. No identifiable information will appear in reports or publications. The project involves no physical risks, as all work will be conducted digitally. Any additional data collection will
comply with university ethics standards and data-sharing agreements.
 
	Project Constraints
	Data Availability and Quality
The accuracy of the AI models depends on the quality of the its data. The main constraint of this project is limited access to real construction datasets, due to data confidentiality. Accordingly, the collected dataset will be leveraged to create synthesized data, helping verify the variables’ presence and ensure their values fall within reasonable ranges. A dataset from A.R. Hourie Enterprises has been secured through our advisors, which we have not yet received for review. To minimize bias, further data from multiple companies will be integrated, avoiding a model that reflects Hourie’s operational characteristics. The current datasets mainly capture residential and commercial projects, consequently the project will focus on these building types to ensure model representativeness.
	Time and Scope Limitations
The project must be completed within the academic year, creating a compressed timeframe that limits in depth data collection and potentially affects the breadth and representativeness of the data that can be incorporated into the model. Given the restricted duration of an academic year, the study will concentrate solely on steel waste in the first phase rather than multiple materials, enabling the team to develop a strong model within the available timeframe.
	Interdisciplinary Knowledge Gap
Incorporating AI into civil engineering presents a learning curve. All team members will be self-learning on the models they utilize for their project work.
	Middle East Operational Context Constraint
Construction practices in the Middle East and the accordingly the model are region-specific. Rebar stock lengths are typically 6 m, 9 m, and 12 m (GGC UAE, 2024), with lead times of 1–3 weeks (Fastmarkets, 2025). Common payment agreements include lump sum followed by unit-rate. DBB contracts dominate, followed by DB (Chambers & Partners, 2025). EPC contracts are excluded, as they apply mainly to industrial megaprojects beyond this project’s scope. When adapting the model to global contexts, the model needs to be revised from the level of data collection, until model selection.
	Implementation Plan and Schedule
The implementation plan outlines the project’s main activities and their sequence throughout the academic year. Tasks will progress from parameter identification and data collection to model training, evaluation, and framework development. Each stage builds on the previous one to ensure a smooth workflow and timely completion. The following Gantt chart presents the detailed timeline and overlap of these tasks.

 

These tasks will be distributed among group members as follows:


	Identify Parameters: Saro Meghdessian, Jad Raad
	Collect Data: Shahan Nadjarian
	Prepare Data: Jad Raad, Lucas Chebly
	Generate Data: All members
	Develop Models: All members
	Evaluate Models: All members
	Application Development: All members
	Build Framework: Lucas Chebly, Saro Meghdessian
 
	Project Resources and Budget
Our project relies mainly on data collected from a regional company, based in Lebanon with the help of our advisors. We will be using the AUB computer labs and our personal laptops to come up with the appropriate algorithm to help reduce construction waste, hence the costs on our project are relatively low.
     

Table 4. Total Cost Breakdown
Item / Resource	Quantity	Unit Cost (USD)	Subtotal (USD)
AI Course (Online)	4	$25	$100
Internet & Cloud Storage (Google Drive / GitHub)	1	$15	$15
Printing & Binding (Final Report)	1	$25	$15
Website Domain Name	1	$20	$20
Total Estimated Cost			≈ $150 USD
 
Acknowledgments
As a group, we would like to thank Dr. Alissar Yehya and Dr. Dima Al Hassanieh for their valuable guidance throughout the weekly meetings and for providing us with all the required resources and direction. A special thanks goes to our advisors, Dr. Mohamed-Asem Abdul Malak and Dr. Farah Dimachkieh, for their constant follow-up, and for the opportunity they provided us by connecting us with one of the biggest construction companies in the region, Entreprises A. R. Hourie, where we were able to collect the data needed for our project.
We would also like to sincerely thank Ms. Karen El Zind, who took the time to meet with us at Hourie Enterprises’ headquarters in Beirut, providing us with guidance and expert input on how steel waste interacts with different parameters, and for giving us access to contracting data that is very difficult to obtain.
Finally, we want to thank Hourie Enterprises for trusting our work and providing us with the data needed to complete our final year project.
 
References
	Adams, K., & Hobbs, G. (2023). Final report: Wastage rates for blocks and ready-mixed concrete. Mineral Products Association (MPA). https://www.mpamasonry.org/MPAMasonry/media/root/assets/MPA-Wastage-Desk-Final-report-01-06-23v3.pdf
	AIA. (2020). Best practices for construction data analytics. American Institute of Architects.
	Ajayi, S. O., Oyedele, L. O., & Akinade, O. O. (2015). Waste effectiveness of the construction industry: Understanding the impediments and requisites of waste reduction. Resources, Conservation & Recycling, 102, 101–112. https://www.sciencedirect.com/science/article/abs/pii/S0921344915300203
	Ajayi, S. O., Oyedele, L. O., Akinade, O. O., Bilal, M., Alaka, H. A., & Owolabi, H. A. (2017). Optimising material procurement for construction waste minimisation. Sustainable Materials and Technologies, 11, 38–46. https://doi.org/10.1016/j.susmat.2017.01.001
	Akinade, O. O., Ajayi, S. O., Oyedele, L. O., Bilal, M., Alaka, H. A., Owolabi, H. A., & Manu, P. (2018). Designing out construction waste using BIM technology. Waste Management, 75, 1–13. https://doi.org/10.1016/j.wasman.2018.02.015
	Akinade, O. O., Oyedele, L. O., Ajayi, S. O., Bilal, M., Alaka, H. A., & Owolabi, H. A., et al. (2018). Designing out construction waste using BIM technology: Stakeholders’ expectations for industry deployment. Journal of Cleaner Production, 180, 375–385. https://www.sciencedirect.com/science/article/pii/S0959652618300283
	Al-Hajj, A., & Hamani, K. (2011). Material waste in the UAE construction industry: Main causes and minimization practices. Architectural Engineering and Design Management, 7(4), 221–235. https://doi.org/10.1080/17452007.2011.594576
	Al-Hajj, A., & Hamani, K. (2011). Material waste in the UAE construction industry. Habitat International, 35(4), 593–601. https://doi.org/10.1016/j.habitatint.2011.03.002
	ASCE. (2020). Data-driven engineering and construction practices. American Society of Civil Engineers.
	Begum, R. A., Siwar, C., Pereira, J. J., & Abd Talib, B. (2009). Waste generation and management in Malaysia construction: A case study. Resources, Conservation and Recycling, 55(2), 302–312. https://doi.org/10.1016/j.resconrec.2008.07.002
	Begum, R. A., Siwar, C., Pereira, J. J., & Jaafar, A. H. (2009). Attitude and behavioral factors in waste management in the construction industry of Malaysia. Resources, Conservation and Recycling, 53(6), 321–328. https://doi.org/10.1016/j.resconrec.2009.01
	Bossink, B. A. G., & Brouwers, H. J. H. (1996). Construction waste: Quantification and source evaluation. Journal of Construction Engineering and Management, 122(1), 55–60. https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9364%281996%29122%3A1%2855%29
	Botchway, E. A., Osei-Tutu, E., Badu, E., & Ahadzie, D. K. (2023). Competencies driving waste minimization during the construction stage of building projects. Buildings, 13(4), 971. https://www.mdpi.com/2075-5309/13/4/971
	Botchway, E. A., et al. (2023). Factors influencing construction waste generation in developing countries. Journal of Cleaner Production. https://www.journals.elsevier.com/journal-of-cleaner-production
	Chambers & Partners. (2025). Construction law in Saudi Arabia. https://practiceguides.chambers.com/practice-guides/construction-law-2025/saudi-arabia
	Cheng, Z., Lu, W., & Xu, J. (2015). Life-cycle construction supply risk: An empirical study. Construction Management and Economics, 33(12), 1083–1098. https://doi.org/10.1080/01446193.2015.1077981
	Ekanayake, L. L., & Ofori, G. (2004). Building waste assessment score: Design-based tool. Building and Environment, 39(7), 851–861. https://doi.org/10.1016/j.buildenv.2004.01.007
	Elsaadany, A., & Elsharawy, A. (2025). Predicting construction waste in Egyptian residential projects using multiple linear regression models. Scientific Reports, 15, Article 86474. https://www.nature.com/articles/s41598-025-86474-1
	Elsadany, A. A., & Elsharawy, M. A. (2025). Predictive models for construction waste in residential projects. Journal of Construction Engineering and Management. https://ascelibrary.org/journal/jcemd4
	Fastmarkets. (2025). Ferrous metals methodology and specifications. https://www.fastmarkets.com/uploads/2025/06/fm-mb-ferrous-metals-methodology-specifications.pdf
	Formoso, C. T., Soibelman, L., De Cesare, C., & Isatto, E. L. (2002). Material waste in building industry: Main causes and prevention. Waste Management, 22(1), 41–46. https://doi.org/10.1016/S0956-053X(02)00007-5
	Formoso, C. T., Soibelman, L., De Cesare, C., & Isatto, E. L. (2002). Material waste in building industry: Main causes and prevention. Journal of Construction Engineering and Management, 128(4), 316–325. https://doi.org/10.1061/(ASCE)0733-9364(2002)
	Fu, X., Li, Z., Chen, H., Li, H., & Wang, Y. (2025). Intelligent optimization method for rebar cutting in pump stations based on BIM and GA. Buildings, 15(11), 1790. https://www.mdpi.com/2075-5309/15/11/1790
	Fu, X., et al. (2025). BIM-integrated genetic algorithm optimization for pump station reinforcement cutting waste. Automation in Construction. https://www.journals.elsevier.com/automation-in-construction
	Gao, Y., Chen, Z., Zhao, X., Xu, Y., & Li, H. (2024). Machine learning in construction and demolition waste management: A comprehensive review (2012–2023). Automation in Construction, 159, 105151. https://www.sciencedirect.com/science/article/abs/pii/S092658052400116X
	Gao, Y., et al. (2024). Machine learning-based prediction of construction and demolition waste. Journal of Cleaner Production. https://www.journals.elsevier.com/journal-of-cleaner-production
	GCC UAE. (2025). Reinforcement bar specifications. https://ggcuae.com/service/reinforcement-bar/
	Hosny, S., Hafez, M., & El-Deeb, H. (2023). Reducing reinforced concrete material waste by BIM implementation: Case study in Egypt. ITcon, 28, 314–333. https://itcon.org/papers/2023-17-ITcon-Hosny.pdf
	Hosny, O., et al. (2023). BIM-based optimization for construction waste minimization. Automation in Construction. https://www.journals.elsevier.com/automation-in-construction
	International Energy Agency. (2024). Energy technology perspectives. https://www.iea.org/reports/energy-technology-perspectives-2024
	International Energy Agency. (2024). Steel industry. https://www.iea.org/energy-system/industry/steel
	Lim, C. H., Ahmed, S., & Ling, F. Y. Y. (2018). Fresh ready-mixed concrete waste in construction projects: A review. Journal of Cleaner Production, 172, 1–12. https://scispace.com/pdf/fresh-ready-mixed-concrete-waste-in-construction-projects-a-1fsn0m3sos.pdf
	Lim, H., et al. (2018). Factors contributing to waste in ready-mix concrete. Journal of Construction Engineering and Management. https://ascelibrary.org/journal/jcemd4
	Olawale, O., & Ayodeji, O. (2022). Material-based penalty-cost quantification model for construction projects influencing waste management. Frontiers in Environmental Science, 9, Article 807359. https://doi.org/10.3389/fenvs.2022.807359
	Olawale, Y., & Ayodeji, E. (2022). Penalty-cost models for construction waste in contracting firms. Construction Management and Economics. https://www.tandfonline.com/toc/rcme20/current
	PMI. (2019). Construction extension to the PMBOK guide. Project Management Institute.
	Poon, C. S., Yu, A. T. W., Wong, S. W., & Cheung, E. (2004). Management of construction waste in public housing projects in Hong Kong. Construction Management and Economics, 22(7), 675–689. https://doi.org/10.1080/0144619042000213292
	Putri, Q. A., et al. (2024). Volume and cutting optimization of reinforcing steel in construction projects. Sustainable Civil Building Management and Engineering Journal, 1(3). https://journal.pubmedia.id/index.php/civilengineering/article/download/2697/2735/5043
	Putri, N., et al. (2024). Cutting-pattern optimization for reinforcement steel. Journal of Construction Engineering. https://ascelibrary.org
	Ren, K., Jia, L., Huang, J., & Wu, M. (2023). Research on cutting-stock optimization of rebar engineering based on BIM and improved PSO. Developments in the Built Environment, 13, 100121. https://www.sciencedirect.com/science/article/pii/S2666165923000030
	Ren, F., et al. (2023). Enhanced PSO approach for rebar cutting optimization. Advanced Engineering Informatics. https://doi.org/10.1016/j.aei.2023.101737
	Salah, A., Omar, R., & Moustafa, A. (2025). Design-stage parameters influencing construction waste generation. Sustainability, 17(17), 7638. https://www.mdpi.com/2071-1050/17/17/7638
	Samal, C. G., et al. (2025). Estimation, classification, and prediction of construction and demolition waste: A machine learning review. Urban Science, 5(1), 10. https://www.mdpi.com/2673-7108/5/1/10
	Samal, P., et al. (2025). Machine learning classification of construction waste at project level. Waste Management. https://www.journals.elsevier.com/waste-management
	Tafesse, S., Esayas Girma, Y., & Dessalegn, E. (2022). Analysis of the socio-economic and environmental impacts of construction waste and management practices. Heliyon, 8(3), e09169. https://doi.org/10.1016/j.heliyon.2022.e09169
	Tam, V. W. Y., Shen, L. Y., & Tam, C. M. (2007). Material wastage in construction activities: A Hong Kong survey. Waste Management & Research, 25(2), 171–181. https://www.researchgate.net/publication/37812483
	Tam, V. W. Y., Tam, C. M., & Le, K. N. (2007). Cutting construction waste by improving material logistics. Waste Management, 27(10), 1590–1598. https://doi.org/10.1016/j.wasman.2006.06.019
	Wang, Z., Zhang, X., & Kim, S. (2024). Minimization of rebar cutting waste using BIM and cutting-pattern-oriented multiobjective optimization. Journal of Construction Engineering and Management, 150(10), 04024143. https://ascelibrary.org/doi/abs/10.1061/JCEMD4.COENG-15104
	Wang, Z., et al. (2024). Multiobjective optimization for rebar cutting patterns. Engineering Structures. https://doi.org/10.1016/j.engstruct.2024
	Widjaja, D. D., & Kim, S. (2023). Reducing rebar cutting waste and rebar usage of beams: A two-stage optimization algorithm. Buildings, 13(9), 2279. https://doi.org/10.3390/buildings13092279
	Widjaja, D. D., Kim, S., & Kwon, K. (2025). Integrating Digital Twin and BIM for special-length-based rebar layout optimization in reinforced concrete construction. Buildings, 15(15), 2617. https://www.mdpi.com/2075-5309/15/15/2617
	Widjaja, Y. D., & Kim, S. (2023). Two-stage optimization algorithm for beam reinforcement cutting. Journal of Building Engineering. https://doi.org/10.1016/j.jobe.2023
	Widjaja, Y. D., et al. (2025). Digital Twin–based optimization for reinforcement layout. Automation in Construction. https://www.journals.elsevier.com/automation-in-construction
	World Steel Association. (2022). World steel in figures. https://worldsteel.org/media-centre/press-releases/2022/world-steel-in-figures-2022
	Yuan, H., & Shen, L. (2011). Trend of the research on construction and demolition waste management. Waste Management, 31(4), 670–679. https://pubmed.ncbi.nlm.nih.gov/21169008/
	WRAP. (2020). Construction material resource efficiency report. Waste and Resources Action Programme.
Appendix 

	Second-semester narrative (source file — paste in main body, not at the end)
The full second-semester chapter is authored in:
	SECOND_SEMESTER_ADDENDUM.md
Do not leave it only at the back of the report. Paste sections 1–13 from that file into the main document immediately after the Concept Summary and before “Background and Project Objectives” (see the placement note under “Second Semester: System Extension and Implementation” near the start of this report). The Appendix entry here is only a pointer to the source file on disk; the printed report should contain the actual text in the early body, not duplicated as a rear appendix unless your instructor requires otherwise.

	Full technical appendix (codebase, APIs, schema, commands)
Complete implementation reference for examiners and handover:
	TECHNICAL_APPENDIX_FULL.md
This file documents repository layout, requirements.txt, data-generation and training pipeline, all 15 model features and categoricals, ModelComparison methods (predict, SHAP/reliability, cost/CO₂), every Flask route, POST /api/predict JSON example, run commands, and production notes. Include it in the final submission as Technical Appendix / Annex C (or merge sections into the Word report).

Data Dictionary
A complete data dictionary has been prepared and stored in the project directory under:
data/data_dictionary.xlsx
This file contains:
	Full list of all input variables used in the synthetic dataset
	Units and engineering definitions
	Parameter ranges and assumed distributions
	Correlation assumptions
	Quality control (QC) checks applied during dataset generation
	Notes on encoding and preprocessing
Additional raw and processed datasets used in this study are stored in the same folder:
	synthetic_steel_waste_parameters.csv
	train_data.csv
	test_data.csv
	full_dataset.csv
These files collectively define the inputs and outputs used during model development and evaluation.

Model Training and Evaluation Code
All core model-related code is stored in the project root and model utilities, including:
	model.py – definition of the machine learning models, training pipeline, and evaluation functions (including the ModelComparison class). Second-semester extensions in this module include explain_prediction (SHAP with fallback to feature importance), calculate_reliability (training-data similarity), and calculate_cost_co2_impact (default steel cost and CO₂ factors).
	data_generation/generate_train_test_data.py – script that loads the raw synthetic dataset, encodes features, and generates the train/test splits.
	app.py – Flask application: form-based and JSON prediction routes, formatting of explainability output for the UI.
This appendix covers:
	Training and evaluation workflow for baseline and advanced models
	Implementation of performance metrics (MAE, RMSE, R², MAPE)
	Project-level splitting logic to avoid data leakage
	Saving of the final trained model (e.g., models/best_steel_waste_model.pkl) for use in the web application
	Post-prediction analytics (explainability, reliability, cost/CO₂) consumed by the web layer and API
Synthetic Data Generation Code

All code used to generate the synthetic steel waste dataset is included in:
data_generation/synthetic_data_generator.py
This appendix includes:
	The complete Python script that generates 5,000–20,000 project samples
	Distribution assumptions and randomization rules
	QC checks performed automatically during generation

Gantt Chart and Schedule
The complete Gantt chart is provided in:
gantt/gantt_chart.pdf
The chart contains:
	Task timeline from Week 1 to Week 12
	Dependencies between major project tasks
	Milestones and decision gates
	Workload distribution among team members

Model Comparison Outputs
All model comparison results are provided in:
data /model_comparison_results.csv
This file includes:
	MAE, RMSE, R², and CV metrics for each machine learning model
	Baseline model performance (fixed allowance, linear regression)
	Hyperparameter comparison notes



Web Application Screenshots & How to Run the App
The live application is the Flask project in the repository root (`app.py`), with HTML templates under `templates/` and static files under `static/`. Install dependencies (see project `requirements.txt` if present), ensure `data/train_data.csv` and `data/test_data.csv` exist or run the data-generation pipeline, then run `python app.py` (default development server; port configured in code, e.g. 5005). Dependencies are listed in `requirements.txt` (including `shap`); use `pip install -r requirements.txt` before running the app.

Screenshots of the updated interface should be stored under:
images/web_application/
Recommended captures:
	Landing page (`/`)
	Prediction form and full results panel (reliability, cost/CO₂, explainability)
	About and Features pages
	Example JSON response from `/api/predict` (for appendix or presentation)

















