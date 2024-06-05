CREATE (john:Person {name: "John Doe", email: "johndoe@example.com", phone: "555-1234", address: "123 Main St, Anytown, USA"})

CREATE (edu1:Education {degree: "B.Sc. in Computer Science", field: "Computer Science", institution: "University X", start_year: 2008, end_year: 2012})
CREATE (edu2:Education {degree: "M.Sc. in Data Science", field: "Data Science", institution: "University Y", start_year: 2013, end_year: 2015})

CREATE (exp1:Experience {position: "Software Developer", company: "Tech Solutions", start_year: 2015, end_year: 2018, description: "Developed software applications."})
CREATE (exp2:Experience {position: "Data Scientist", company: "Data Analytics Inc.", start_year: 2018, end_year: 2023, description: "Worked on data analysis and machine learning models."})

CREATE (skill1:Skill {name: "Python", proficiency: "Expert"})
CREATE (skill2:Skill {name: "Machine Learning", proficiency: "Advanced"})

CREATE (project1:Project {name: "E-commerce Recommendation System", description: "Developed a recommendation system for an e-commerce platform.", technologies: "Python, Scikit-Learn", start_year: 2019, end_year: 2020})

CREATE (cert1:Certification {name: "Certified Data Scientist", institution: "Data Science Academy", year: 2020})

CREATE (course1:Course {name: "Machine Learning", institution: "Coursera", year: 2019})

CREATE (john)-[:STUDIED_AT]->(edu1)
CREATE (john)-[:STUDIED_AT]->(edu2)
CREATE (john)-[:WORKED_AT]->(exp1)
CREATE (john)-[:WORKED_AT]->(exp2)
CREATE (john)-[:HAS_SKILL]->(skill1)
CREATE (john)-[:HAS_SKILL]->(skill2)
CREATE (john)-[:WORKED_ON]->(project1)
CREATE (john)-[:HAS_CERTIFICATION]->(cert1)
CREATE (john)-[:COMPLETED_COURSE]->(course1)
CREATE (edu1)-[:CONFERRED_SKILL]->(skill1)
CREATE (edu2)-[:CONFERRED_SKILL]->(skill2)
CREATE (exp1)-[:USED_SKILL]->(skill1)
CREATE (exp2)-[:USED_SKILL]->(skill2)
CREATE (project1)-[:USED_SKILL]->(skill1)



// Find all skills acquired during education
MATCH (john:Person {name: "John Doe"})-[:STUDIED_AT]->(edu:Education)-[:CONFERRED_SKILL]->(skill:Skill)
RETURN skill.name AS Skill, edu.institution AS Institution


// List jobs where a specific skill was used
MATCH (john:Person {name: "John Doe"})-[:WORKED_AT]->(exp:Experience)-[:USED_SKILL]->(skill:Skill {name: "Python"})
RETURN exp.position AS Position, exp.company AS Company


//Find all projects worked on along with technologies used
MATCH (john:Person {name: "John Doe"})-[:WORKED_ON]->(project:Project)
RETURN project.name AS Project, project.technologies AS Technologies

// List all certifications
MATCH (john:Person {name: "John Doe"})-[:HAS_CERTIFICATION]->(cert:Certification)
RETURN cert.name AS Certification, cert.institution AS Institution, cert.year AS Year


// Find all courses completed
MATCH (john:Person {name: "John Doe"})-[:COMPLETED_COURSE]->(course:Course)
RETURN course.name AS Course, course.institution AS Institution, course.year AS Year
