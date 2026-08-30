"""All human-editable site content lives here.

Why a Python file instead of YAML: no extra dependency, real comments, and
triple-quoted strings survive line breaks without indentation games.

Publications are NOT here - they come from src/data/publications.bib.

PRIVACY NOTE: the CV PDF also contains a home address, a mobile number and the
phone numbers / e-mails of three referees. Those are deliberately NOT copied to
this file, because this content is published on the open web.
"""

# --------------------------------------------------------------------------
# Identity and contact
# --------------------------------------------------------------------------
SITE = {
    "name": "Zeyin Yan",
    "role": "Associate Professor",
    "institute": "Institute of Nanotechnology and Intelligence (inAI)",
    "university": "Jinan University",
    "city": "Guangzhou",
    "country": "P.R. China",
    "email": "zeyin.yan@outlook.com",
    "base_url": "https://yanjordan.github.io",
    "cv_pdf": "research/Zeyin_YAN_CV_EN.pdf",
    "description": (
        "Zeyin Yan - Associate Professor at the Institute of Nanotechnology and "
        "Intelligence (inAI), Jinan University. Multiscale simulation of "
        "nanomedicine, machine learning for physics-based modelling, and "
        "Bayesian optimization for materials and formulation design."
    ),
    "keywords": (
        "Zeyin Yan, nanomedicine, multiscale simulation, DFT, molecular dynamics, "
        "dissipative particle dynamics, machine learning potential, Bayesian "
        "optimization, quantum refinement, drug delivery, Jinan University, inAI"
    ),
    # og:image is used when the site is shared on WeChat / X / LinkedIn.
    "og_image": "research/NC2024.jpg",
}

# Text links on purpose: the old site pulled Font Awesome from a retired
# use.fontawesome.com kit, which can disappear without warning. Plain text has
# no external dependency and cannot break.
LINKS = [
    {"label": "Email", "url": "mailto:zeyin.yan@outlook.com"},
    {"label": "ORCID", "url": "https://orcid.org/0000-0003-3359-7547"},
    {"label": "Web of Science", "url": "https://www.webofscience.com/wos/author/record/T-5967-2018"},
    {"label": "ResearchGate", "url": "https://www.researchgate.net/profile/Zeyin-Yan"},
    {"label": "GitHub", "url": "https://github.com/YanJordan"},
    # TODO(zeyin): add your Google Scholar profile URL here - it matters more than
    # ResearchGate for academic visibility. Left out rather than guessed.
    # {"label": "Google Scholar", "url": "https://scholar.google.com/citations?user=XXXX"},
]

# --------------------------------------------------------------------------
# Navigation. `file` is the generated HTML file name.
# --------------------------------------------------------------------------
NAV = [
    {"label": "Home", "file": "index.html"},
    {"label": "Research", "file": "research.html"},
    {"label": "Publications", "file": "publications.html"},
    {"label": "Code", "file": "code.html"},
    {"label": "CV", "file": "cv.html"},
    {"label": "News", "file": "news.html"},
    {"label": "Teaching", "file": "teaching.html"},
    {"label": "Join us", "file": "join.html"},
]

# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------
HOME = {
    # Rewritten: the previous version had a dangling sentence fragment
    # ("After post-doc and senior research fellowships ... at the SUSTech.")
    # and spelled Physics as "Physic".
    "bio": """
      I am an Associate Professor at the
      <a href="https://www.jnu.edu.cn/" target="_blank" rel="noopener noreferrer">Jinan University</a>
      Institute of Nanotechnology and Intelligence (inAI), in Guangzhou, China.
      Before joining Jinan University I spent six years at the
      <a href="https://www.sustech.edu.cn/en/" target="_blank" rel="noopener noreferrer">Southern University of Science and Technology</a>
      (SUSTech) as a post-doctoral fellow and then Senior Research Fellow in the
      <a href="https://chem.sustech.edu.cn/" target="_blank" rel="noopener noreferrer">Department of Chemistry</a>,
      working with Prof. Lung Wa Chung. I received my PhD in Physics from
      <a href="https://www.centralesupelec.fr/" target="_blank" rel="noopener noreferrer">CentraleSup&eacute;lec, Universit&eacute; Paris-Saclay</a>
      in 2018, supervised by Prof. Jean-Michel Gillet.
    """,
    "focus_heading": "What I work on now",
    "focus": """
      My group builds computational methods for <strong>nanomedicine</strong>. We
      combine multiscale physics-based simulation &mdash; electronic structure
      (DFT), all-atom molecular dynamics, and coarse-grained / dissipative
      particle dynamics (DPD) &mdash; with <strong>machine learning</strong> and
      <strong>Bayesian optimization</strong>. The aim is to make the design of
      nanocarriers and drug-delivery systems something we can predict and
      optimize, instead of something we find by trial and error.
    """,
    # This paragraph was already on the old site and is worth keeping; only the
    # grammar was tightened.
    "philosophy": """
      Theoretical computation is a model that describes nature, and each
      experiment yields a projection of nature from one particular point of view.
      I believe a general model that combines theoretical computation with
      multiple experimental observations can bring us closer to nature &mdash;
      much as a 3D object can be reconstructed from a set of 2D images.
    """,
    "figures": [
        {
            "src": "research/QR2021.png",
            "caption": "Multiscale quantum refinement: a joint model for refining protein structures.",
            "alt": "Workflow of multiscale quantum refinement for metalloproteins",
        },
        {
            "src": "research/NC2024.jpg",
            "caption": "Machine learning removes the quantum-mechanical bottleneck in refining protein-drug systems.",
            "alt": "Machine-learning accelerated quantum refinement of protein-drug systems",
        },
        {
            "src": "Electron_density.jpg",
            "caption": "Joint model for electron density, connecting position-space and momentum-space observables.",
            "alt": "Joint refinement model linking charge, spin and momentum densities",
        },
    ],
}

# --------------------------------------------------------------------------
# Research page. `thrusts` = the new direction, `foundations` = what it builds on.
# --------------------------------------------------------------------------
RESEARCH = {
    "intro": """
      Nanomedicine is where my methods work is heading. A nanocarrier is hard to
      model for a simple reason: the properties that decide whether it works
      &mdash; self-assembly, drug loading, stability, release, interaction with
      membranes and proteins &mdash; live on different length and time scales, and
      no single method covers all of them. The three directions below are my
      answer to that problem: get the scales to talk to each other, use machine
      learning where exact physics is too slow, and let optimization decide which
      experiment to run next.
    """,
    "thrusts": [
        {
            "title": "Multiscale simulation of nanomedicine",
            "tag": "Physics-based modelling",
            "body": """
              Lipid nanoparticles, polymeric micelles and metal-organic
              frameworks each demand a different resolution. We build workflows
              that pass information between electronic structure theory (DFT),
              all-atom molecular dynamics, and coarse-grained / dissipative
              particle dynamics (DPD), so that formulation-level questions can be
              answered from physics: what does this carrier self-assemble into,
              where does the payload sit, and what makes it come out again?
            """,
            "keywords": ["DFT", "all-atom MD", "coarse-grained models", "DPD", "self-assembly", "drug release"],
        },
        {
            "title": "Machine learning for physics-based simulation",
            "tag": "ML + first principles",
            "body": """
              Accurate quantum methods are too expensive for the system sizes and
              time scales that matter in drug delivery. In
              <a href="publications.html">Yan et al., Nat. Commun. 2024</a> we
              replaced the quantum-mechanical bottleneck inside multiscale
              quantum refinement with a machine-learning potential, making
              reliable refinement of protein-drug complexes affordable. We keep
              pushing this line: ML potentials, learned physical descriptors
              (such as the local-distortion indices from
              <a href="code.html">D2AF</a>), and surrogate models that preserve
              the physics while dropping the cost.
            """,
            "keywords": ["ML potentials", "QM/MM acceleration", "descriptors", "surrogate models", "&Delta;-learning"],
        },
        {
            "title": "Bayesian optimization for design and discovery",
            "tag": "Closed-loop experimental design",
            "body": """
              Designing a nanoformulation is a mixed-variable, multi-objective
              problem: continuous component ratios, categorical lipid or ligand
              identities, boolean process switches, and objectives that genuinely
              conflict &mdash; encapsulation efficiency against particle size
              against stability against toxicity. We develop Bayesian
              optimization tooling built for that setting: mixed search spaces,
              single- and multi-objective acquisition functions (including
              hypervolume-based qNEHVI), and a uniform suggest/observe interface
              that plugs into real experimental campaigns. The target is a closed
              loop &mdash; the model proposes the next batch, the bench returns
              the data, and the loop tightens.
            """,
            "keywords": ["Bayesian optimization", "mixed variables", "multi-objective", "qNEHVI", "active learning", "self-driving lab"],
        },
    ],
    "foundations_heading": "Foundations",
    "foundations_intro": """
      The directions above stand on earlier work in multiscale quantum chemistry
      and quantum crystallography. Full details are on the
      <a href="publications.html">publications</a> page.
    """,
    "foundations": [
        {
            "title": "Quantum refinement of biomacromolecules",
            "body": """
              Refining protein and protein-drug structures against X-ray data
              while keeping the chemistry honest, using QM/MM and ONIOM-based
              multiscale models.
            """,
            "refs": "J. Chem. Theory Comput. 2021; Nat. Commun. 2024",
        },
        {
            "title": "Charge, spin and momentum densities",
            "body": """
              Joint refinement of complementary experiments (X-ray diffraction,
              polarized neutron diffraction, magnetic Compton scattering) to
              reconstruct the one-electron reduced density matrix, in both
              position and momentum space.
            """,
            "refs": "Phys. Rev. B 2017 (I &amp; II); Acta Cryst. A 2018; J. Chem. Phys. 2018; IUCrJ 2019",
        },
        {
            "title": "Quantum tunnelling under external electric fields",
            "body": """
              How an applied electric field steers heavy-atom tunnelling, and
              what that means for reactivity and selectivity.
            """,
            "refs": "J. Phys. Chem. Lett. 2023",
        },
        {
            "title": "Local distortion analysis",
            "body": """
              An atom-resolved decomposition of distortion energy that turns the
              distortion/interaction model into a distortion map, and yields
              indices usable as ML descriptors.
            """,
            "refs": "Chem. Sci. 2025",
        },
    ],
}

# --------------------------------------------------------------------------
# Code page. Every URL below was checked and returns HTTP 200.
# --------------------------------------------------------------------------
CODE = {
    "intro": """
      Code from my papers, plus tools I keep coming back to. Most of it is
      research code: usable, but written for a purpose rather than for a product.
    """,
    "groups": [
        {
            "language": "Python",
            "items": [
                {
                    "name": "D2AF",
                    "summary": "Distortion distribution analysis by fragmentation - decomposes distortion energy to individual atoms and produces a distortion map.",
                    "links": [
                        {"label": "GitHub", "url": "https://github.com/oscarchung-lab/D2AF"},
                        {"label": "PyPI", "url": "https://pypi.org/project/D2AF/"},
                    ],
                    "paper": "Chem. Sci. 2025, 16, 2351-2362",
                    "paper_doi": "10.1039/d4sc07226j",
                },
                {
                    "name": "ECHG",
                    "summary": "Python GUI for electron charge density maps (a port of the earlier MATLAB GUI).",
                    "links": [{"label": "GitHub", "url": "https://github.com/yanjordan/ECHG"}],
                },
                {
                    "name": "Pymol_scripts",
                    "summary": "Helper scripts for PyMOL, mostly for setting up and inspecting QM/MM models.",
                    "links": [{"label": "GitHub", "url": "https://github.com/yanjordan/Pymol_scripts"}],
                },
            ],
        },
        {
            "language": "Fortran",
            "items": [
                {
                    "name": "ONIOM_QR_mod",
                    "summary": "ONIOM-based quantum refinement code for metalloproteins and protein-drug systems.",
                    "links": [{"label": "GitHub", "url": "https://github.com/YanJordan/ONIOM_QR_mod"}],
                    "paper": "J. Chem. Theory Comput. 2021, 17, 3783-3796; Nat. Commun. 2024, 15, 4181",
                    "paper_doi": "10.1021/acs.jctc.1c00148",
                },
                {
                    "name": "QT_Polyrate17_Gaussrate17_Mod",
                    "summary": "Modified Polyrate / Gaussrate for tunnelling rate calculations under an external electric field.",
                    "links": [{"label": "GitHub", "url": "https://github.com/YanJordan/QT_Polyrate17_Gaussrate17_Mod"}],
                    "paper": "J. Phys. Chem. Lett. 2023, 14, 1124-1132",
                    "paper_doi": "10.1021/acs.jpclett.2c03461",
                },
                {
                    "name": "Cluster_Model_Cry14",
                    "summary": "Cluster model for computing density matrices and related properties from CRYSTAL14 output.",
                    "links": [{"label": "GitHub", "url": "https://github.com/yanjordan/Cluster_Model_Cry14"}],
                    "paper": "J. Chem. Phys. 2018, 148, 164106; Acta Cryst. A 2018, 74, 131-142",
                    "paper_doi": "10.1063/1.5022770",
                },
            ],
        },
        {
            "language": "MATLAB",
            "items": [
                {
                    "name": "MATLAB_GUI_ED",
                    "summary": "GUI for electron density maps (CRYSTAL, Gaussian), density matrices, Moyal functions, Compton profiles and momentum density reconstruction.",
                    "links": [{"label": "GitHub", "url": "https://github.com/yanjordan/MATLAB_GUI_ED"}],
                },
            ],
        },
        {
            "language": "Gaussian utilities",
            "items": [
                {
                    "name": "Gaussian_ext",
                    "summary": "External interfaces from Gaussian to other programs, plus assorted tools for Gaussian calculations.",
                    "links": [{"label": "GitHub", "url": "https://github.com/yanjordan/Gaussian_ext"}],
                },
            ],
        },
    ],
}

# --------------------------------------------------------------------------
# CV page. Extracted from research/Zeyin_YAN_CV_EN.pdf and the publication list.
# Home address, mobile number and referees' contact details are intentionally
# omitted - see the privacy note at the top of this file.
# --------------------------------------------------------------------------
CV = {
    "intro": """
      A web version of my CV. The
      <a href="research/Zeyin_YAN_CV_EN.pdf">PDF version</a> is also available.
    """,
    "appointments": [
        {
            "period": "2026 &ndash; present",
            "role": "Associate Professor",
            "org": "Institute of Nanotechnology and Intelligence (inAI), Jinan University",
            "place": "Guangzhou, China",
            "detail": "Multiscale simulation of nanomedicine; machine learning and Bayesian optimization for formulation and materials design.",
        },
        {
            "period": "2020.12 &ndash; 2026",
            "role": "Senior Research Fellow",
            "org": "Department of Chemistry, Southern University of Science and Technology",
            "place": "Shenzhen, China",
            "detail": "Group of Prof. Lung Wa Chung. Quantum tunnelling under electric fields; machine-learning-accelerated quantum refinement for drug design.",
        },
        {
            "period": "2018.11 &ndash; 2020.11",
            "role": "Post-doctoral Fellow",
            "org": "Department of Chemistry, Southern University of Science and Technology",
            "place": "Shenzhen, China",
            "detail": "Group of Prof. Lung Wa Chung. Assessment of multiscale quantum refinement approaches for metalloproteins.",
        },
        {
            "period": "2018.05 &ndash; 2018.10",
            "role": "Visiting Researcher",
            "org": "Department of Chemistry, Southern University of Science and Technology",
            "place": "Shenzhen, China",
            "detail": "Group of Prof. Lung Wa Chung.",
        },
    ],
    "education": [
        {
            "period": "2015.01 &ndash; 2018.01",
            "degree": "PhD in Physics",
            "org": "CentraleSup&eacute;lec, Universit&eacute; Paris-Saclay (Laboratoire SPMS)",
            "place": "Paris, France",
            "detail": "Thesis: 2D magnetic momentum density reconstruction and determination of the one-electron reduced density matrix. Supervisor: Prof. Jean-Michel Gillet.",
        },
        {
            "period": "2012.09 &ndash; 2015.01",
            "degree": "MSc, Information and Computing Sciences / Telecommunication (double major)",
            "org": "Beihang University",
            "place": "Beijing, China",
            "detail": "Thesis: single-photon laser radar imaging based on the QSI protocol. Supervisor: Prof. Jie Chen.",
        },
        {
            "period": "2008.09 &ndash; 2012.06",
            "degree": "BSc, Information and Computing Sciences",
            "org": "Beihang University",
            "place": "Beijing, China",
            "detail": "Project: materials with high thermal but low electrical conductivity. Supervisor: A/Prof. Hongzhe Tang.",
        },
    ],
    "funding": [
        {
            "period": "2023 &ndash; 2026",
            "title": "Combining machine learning with quantum refinement methods for protein-drug structures",
            "org": "Natural Science Foundation of Shenzhen Innovation Committee",
            "detail": "CNY 300k. Main participant.",
        },
    ],
    "talks": [
        {
            "year": "2017",
            "title": "Electron representations in phase space by a cluster approach",
            "venue": "8th International Conference on Theory of Atomic &amp; Molecular Clusters, Beijing, China",
        },
        {
            "year": "2017",
            "title": "Quantum crystallography in spin-resolved phase space",
            "venue": "CECAM Discussion Meeting on Quantum Crystallography, Nancy, France",
        },
        {
            "year": "2016",
            "title": "Quantum modelling of magnetic scattering experiments",
            "venue": "Colloque de Recherche Inter Ecoles Centrales, Paris, France",
        },
        {
            "year": "2016",
            "title": "Probability densities in different spaces: when the multipolar-atom model is just not enough",
            "venue": "European Crystallographic Meeting, Basel, Switzerland",
        },
    ],
    "skills": [
        {
            "label": "Programming",
            "items": "Python, Fortran, Shell, MATLAB, OpenMP, MPI, LaTeX",
        },
        {
            "label": "Machine learning / optimization",
            "items": "PyTorch, scikit-learn, Gaussian processes, Bayesian optimization (BoTorch, HEBO), ML potentials (MLatom, TorchANI)",
        },
        {
            "label": "Quantum chemistry",
            "items": "Gaussian, ORCA, CP2K, MolPro, CRYSTAL14, Multiwfn, AIMAll, Bader, Polyrate",
        },
        {
            "label": "Biomolecular / materials simulation",
            "items": "GROMACS, Schr&ouml;dinger, PyMOL, CNS, MoPro, Mercury, VESTA, Molekel",
        },
        {
            "label": "Computing",
            "items": "Linux, HPC scheduling, GPU computing",
        },
        {
            "label": "Languages",
            "items": "Chinese (native), English (fluent), French (working knowledge)",
        },
    ],
    "referees_note": """
      Referee details are available on request.
    """,
}

# --------------------------------------------------------------------------
# Placeholder pages. Structure is ready; fill in when you have content.
# --------------------------------------------------------------------------

# To add an item:
#   {"date": "2026-09-01", "body": "Joined inAI, Jinan University."},
NEWS = []
NEWS_EMPTY = "Nothing posted yet."

TEACHING = {
    "intro": "",
    "courses": [],
    # Example:
    # "courses": [{
    #     "code": "CHEM xxx",
    #     "title": "Computational Chemistry",
    #     "term": "Spring 2027",
    #     "level": "Undergraduate",
    #     "body": "Short description.",
    # }],
    "empty": "Course information will appear here.",
}

JOIN = {
    "intro": "",
    "positions": [],
    # Example:
    # "positions": [{
    #     "title": "PhD students (2027 intake)",
    #     "body": "What the project is about and what background helps.",
    # }],
    "empty": "Openings will be posted here.",
}
