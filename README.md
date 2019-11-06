# Resume-and-Job-Description-Similarity-Api
It matches the Cosine Similarity between two documents.
input ==>>
{
"resume_directory":"D:\\resume scanner\\resume_for_test",
"jd_directory":"D:\\resume scanner\\jd_for_test"
}

Output ==>>
[
    {
        "Job Description": "Google ml_jd.pdf",
        "Resume": "Resume --Rohini Prakash.pdf",
        "Resume Ratch Score": "40.52%"
    },
    {
        "Job Description": "Google ml_jd.pdf",
        "Resume": "Rohini Prakash.docx",
        "Resume Ratch Score": "40.410000000000004%"
    },
    {
        "Job Description": "Google ml_jd.pdf",
        "Resume": "test_resume.pdf",
        "Resume Ratch Score": "56.82000000000001%"
    },
    {
        "Job Description": "Machine-Learning-Engineer.pdf",
        "Resume": "Resume --Rohini Prakash.pdf",
        "Resume Ratch Score": "58.32000000000001%"
    },
    {
        "Job Description": "Machine-Learning-Engineer.pdf",
        "Resume": "Rohini Prakash.docx",
        "Resume Ratch Score": "57.78%"
    },
    {
        "Job Description": "Machine-Learning-Engineer.pdf",
        "Resume": "test_resume.pdf",
        "Resume Ratch Score": "61.23%"
    }
]
