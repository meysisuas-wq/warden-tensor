# Contributing to WardenTensor

1. Fork → Clone → Branch → Code → Test → PR

## Development
```bash
git clone https://github.com/YOUR_USERNAME/warden-tensor.git
cd warden-tensor
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Style
- Black (100), isort, Ruff
- Type hints required
- Conventional commits

## Security
- Never commit API keys
- Test with diverse datasets
- Document false positive rates

## License
MIT
