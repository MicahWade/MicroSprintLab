# MicroSprintLab

**MicroSprintLab** helps coders hone their programming skills with short, focused 1-hour projects—ideal for anyone learning programming languages or fundamentals.

## 🎯 Who Is This For?

MicroSprintLab is built for coders of all levels who want to:

- Build and practice programming skills efficiently  
- Explore new programming languages  
- Strengthen programming fundamentals

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MicahWade/MicroSprintLab.git ~/Documents/
cd ~/Documents/MicroSprintLab/
```

### 2. Set Up the Python Environment

Create a virtual environment:
```bash
python -m venv venv
```

Activate it:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

Install requirements:
```bash
pip install -r requirements.txt
```

### 3. Configure Your Editor

- Open `setting.json` and set your preferred editor.

### 4. Launch MicroSprintLab

```bash
python3 main.py
```

## 📝 Neovim Integration (Optional)

**Prerequisite:** First complete the [Getting Started](#getting-started) steps above.

1. **Enable Neovim support:**  
   In `setting.json`, set:
   ```json
   "nvim": true
   ```

2. **Install Lua Plugin:**
   ```bash
   cp ~/Documents/MicroSprintLab/microsprintlab.lua ~/.config/nvim/lua/microsprintlab.lua
   ```

3. **Update Your `init.lua`:**
   Add:
   ```lua
   require("microsprintlab").setup()
   ```

4. **Start MicroSprintLab from Neovim:**
   ```
   :MicroSprintLab
   ```

## MicroSprintLab Wiki

- [Settings](settings) — Details about configuration settings available.
- [Customization Guide](Customization-Guide) — Learn how to adjust non-core settings.
- [Ideas](Ideas) — How to Add Ideas.

## TODO

- [ ] Add language boilerplate template for new files.
- [ ] Implement different modes for timed projects, e.g.:
  - 2-hour sessions
  - 30-minute sprints
  - Feature implementation on someone else's project within a set time
- [ ] Support additional editors besides Neovim.
- [ ] Add more ideas and enhancements.

## 🤝 Contributing

- Some parts of the codebase are AI-generated.
- **Do:**
    - Add new ideas to `idea.json`
    - Help with Lua and Neovim integration
    - Submit editor support (must be fully functional before merging)
    - Report bugs clearly, with steps to reproduce
- **Don't:**
    - Use AI for code changes (all modifications should be human-written and clearly explained)

## ⚠️ Known Issues

- There are currently no known issues or limitations.
