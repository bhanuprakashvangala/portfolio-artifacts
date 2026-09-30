# Portfolio artifacts

Project materials and runnable companion examples for [Bhanu Prakash Vangala’s academic portfolio](https://bhanuprakashvangala.github.io/).

Each project has an overview, an image or system diagram, and links to available source code and reports. Existing public repositories remain the authoritative code locations. Where original code is not public, the project page identifies the available materials and the scope of any new example.

## Project catalog

| Project | Available artifact |
| --- | --- |
| [Image Colorization using AI](projects/image-colorization) | Documentation + materials |
| [Multilingual Sentiment Analysis on KOO User Posts](projects/koo) | Companion example |
| [LLM-as-a-Service](projects/llm-service-thesis) | Original repository |
| [Brain Tumor Detection in MRI Images using Transfer Learning](projects/brain-tumor-project) | Companion example |
| [Pneumonia Detection on X-ray Images Using Deep Learning](projects/pneumonia-project) | Companion example |
| [LearnLLM.dev](projects/learnllm) | Documentation + materials |
| [VisionAI: AI assistance for visually impaired users](projects/visionai) | Original repository |
| [ReflectMemory: persistent memory for long-context reasoning](projects/reflectmemory) | Companion example |
| [Autonomous indoor navigation](projects/indoor-nav) | Companion example |
| [ChatMed: grounded medical question answering](projects/chatmed) | Original repository |
| [CropInsight: crop health and yield forecasting](projects/cropinsight) | Original repository |
| [SocialSift: crisis-aware multilingual sentiment analysis](projects/socialsift) | Original repository |
| [FlexiFlow: Bandit-based Model Switching in ML Workflows](projects/flexiflow) | Companion example |
| [TRACE: A Programmable Cloud Laboratory for Autonomous Experimentation](projects/trace) | Documentation + materials |
| [Reproducible Containers for Advancing Process-oriented Collaborative Analytics](projects/reproducible-containers) | Documentation + materials |
| [Book Recommendation System](projects/book-recommendation) | Original repository |

## Run the examples

Python 3.10+ is sufficient; there are no third-party dependencies.

```sh
python examples/evaluate.py examples/data/predictions.csv
python examples/navigation.py examples/data/floor.json entrance lab
python examples/routing.py --rounds 1000 --seed 7
python examples/memory.py notes.db add "Kubernetes deployment notes"
python examples/memory.py notes.db search "deployment"
python -m unittest discover -s tests -v
```

See [input formats and limitations](examples/README.md). The four examples are newly written educational/reference implementations. They do not reproduce published experiments, and their synthetic data are not research evidence. Reports, datasets, images, and linked repositories retain their existing rights and licenses.
