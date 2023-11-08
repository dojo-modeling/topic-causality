
# Causal[ity] Recommender API

Make requests, issuing a topic, and receiving causes and/or effects of the given topic!

# Initial setup

If interested on using your device GPU to run the docker container, leave this setup in:

```yaml
deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

If not, comment it out and the recommender engine will run on CPU (slower to run, but less setup to get started).

Selecting the GPU setup requires:
- A GPU available on the host device running the container
- GPU drivers installed. If nvidia on ubuntu, you'll need the `nvidia-driver-<version>` packages installed.
- For nvidia, you'll need the `nvidia-container-runtime` installed.

For a full guide and references, See `doc/setting-docker-service-gpu.md` on this repository.

### Examples

##### Request

```bash
curl --request POST \
  --url http://0.0.0.0:8084/causal-recommender/causes \
  --header 'Content-Type: application/json' \
  --data '{
	"topic": "privacy paranoia"
    }'
```

##### Response

```json
{
	"causes": [
		"chemical contamination in the food supply",
		"loss of privacy",
		"fluoride in",
		"government control",
		"nuclear proliferation",
		"the media's lies",
		"chemtrails/fog",
		"global warming",
		"NSA spying"
	]
}
```

# Running

```bash
docker-compose up
```

If using outside of docker, ensure  the `TRANSFORMERS_CACHE` environment variable is set to yur preferred cache location. Else, it will default to `$HOME/.cache/huggingface`

### Note

The following shared volume is set up by default:
- ./big_models_data_cache:/recommender/big_models_data_cache

with the following env var set on Dockerfile:

```
ENV TRANSFORMERS_CACHE="/recommender/big_models_data_cache"
```

Which means that, by default, the host will contain this model cache as well. This makes it so that the container can be stopped, rebuilt, or restarted and the 6.5GB model can be reused between sessions.

If running on docker, you may add instead a `.env` file with:

```
TRANSFORMERS_CACHE="/recommender/big_models_data_cache"
```

You may also add other configurations to work with your gpu and max gpu-memory allocation, such as:

```
PYTORCH_CUDA_ALLOC_CONF=backend:native,max_split_size_mb:10
```
