import time
import pynvim
import os


def DrawFloatingWindowWithTimer(textLines, timeoutSec):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, textLines)

    width = max(len(line) for line in textLines) + 2 if textLines else 10
    height = len(textLines) if textLines else 1

    screenWidth = nvim.api.get_option("columns")
    screenHeight = nvim.api.get_option("lines")

    row = (screenHeight - height) // 2
    col = (screenWidth - width) // 2
    opts = {
        "relative": "editor",
        "width": width,
        "height": height,
        "row": row,
        "col": col,
        "style": "minimal",
        "border": "single",
    }

    win = nvim.api.open_win(buf, True, opts)

    nvim.api.buf_set_keymap(
        buf, "n", "q", ":close<CR>", {"nowait": True, "noremap": True, "silent": True}
    )
    nvim.api.buf_set_keymap(
        buf,
        "n",
        "<ESC>",
        ":close<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )

    nvim.exec_lua("""
    function ClosePopup(win_id)
        if vim.api.nvim_win_is_valid(win_id) then
        vim.api.nvim_win_close(win_id, true)
        end
    end
    """)

    nvim.command(f"""
    function! ClosePopupWrapper(timer_id)
      lua ClosePopup({win.handle})
      call timer_stop(a:timer_id)
    endfunction
    """)

    nvim.call("timer_start", int(timeoutSec * 1000), "ClosePopupWrapper")


def DisplayFullscreenTextWithTimer(textLines, timeoutSec):
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, textLines)
    width = max(len(line) for line in textLines) + 2 if textLines else 10
    height = len(textLines) if textLines else 1
    screenWidth = nvim.api.get_option("columns")
    screenHeight = nvim.api.get_option("lines")
    opts = {
        "relative": "editor",
        "width": screenWidth,
        "height": screenHeight,
        "row": 0,
        "col": 0,
        "style": "minimal",
        "border": "single",
    }
    win = nvim.api.open_win(buf, True, opts)
    nvim.api.buf_set_keymap(
        buf, "n", "q", ":close<CR>", {"nowait": True, "noremap": True, "silent": True}
    )
    nvim.api.buf_set_keymap(
        buf,
        "n",
        "<ESC>",
        ":close<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )
    nvim.exec_lua("""
    function ClosePopup(win_id)
        if vim.api.nvim_win_is_valid(win_id) then
            vim.api.nvim_win_close(win_id, true)
        end
    end
    """)
    nvim.command(f"""
    function! ClosePopupWrapper(timer_id)
        lua ClosePopup({win.handle})
        call timer_stop(a:timer_id)
    endfunction
    """)
    nvim.call("timer_start", int(timeoutSec * 1000), "ClosePopupWrapper")


def OpenFileInSingleTab(filePath):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    currentTab = nvim.api.get_current_tabpage()
    for tab in nvim.api.list_tabpages():
        if tab != currentTab:
            nvim.api.tabpage_close(tab, True)

    nvim.command(f"edit {filePath}")

    absPath = os.path.abspath(filePath)
    directory = os.path.dirname(absPath)
    nvim.command(f"cd {directory}")

    curBuf = nvim.api.get_current_buf()
    for b in nvim.api.list_bufs():
        if b != curBuf:
            try:
                nvim.api.buf_delete(b, {"force": True})
            except Exception:
                pass

    # Set window options to enable line numbers, relative line numbers, and sign column
    curWin = nvim.api.get_current_win()
    nvim.api.win_set_option(curWin, "number", True)
    nvim.api.win_set_option(curWin, "relativenumber", True)
    nvim.api.win_set_option(curWin, "signcolumn", "yes")


def CloseNvim():
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    currentTab = nvim.api.get_current_tabpage()
    for tab in nvim.api.list_tabpages():
        if tab != currentTab:
            nvim.api.tabpage_close(tab, True)


def FullscreenCountdownWithText(text, seconds):
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    buf = nvim.api.create_buf(False, True)
    screenWidth = nvim.api.get_option("columns")
    screenHeight = nvim.api.get_option("lines")
    opts = {
        "relative": "editor",
        "height": screenHeight,
        "width": screenWidth,
        "row": 0,
        "col": 0,
        "style": "minimal",
        "border": "single",
    }
    win = nvim.api.open_win(buf, True, opts)
    nvim.api.buf_set_keymap(
        buf,
        "n",
        "<CR>",
        ":lua _close_countdown_popup()<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )
    nvim.api.buf_set_keymap(
        buf,
        "n",
        "q",
        ":lua _close_countdown_popup()<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )
    nvim.api.buf_set_keymap(
        buf,
        "n",
        "<ESC>",
        ":lua _close_countdown_popup()<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )
    nvim.exec_lua("""
    vim.g.countdown_break = false
    function _close_countdown_popup()
        vim.g.countdown_break = true
    end
    """)
    for remaining in range(seconds, 0, -1):
        textLines = str(text).splitlines()
        linesToSet = textLines + [f"Countdown: {remaining}"]
        nvim.api.buf_set_lines(buf, 0, -1, False, linesToSet)
        if nvim.exec_lua("return vim.g.countdown_break"):
            break
        time.sleep(1)
    nvim.api.win_close(win, True)
    return nvim.exec_lua("return vim.g.countdown_break")


def DisplayTextWait(textLines):
    if isinstance(textLines, str):
        textLines = textLines.splitlines() or [textLines]
    elif isinstance(textLines, (list, tuple)):
        textLines = [str(line) for line in textLines]
    else:
        raise TypeError("textLines must be a string or list/tuple of strings")

    nvim = pynvim.attach("socket", path="/tmp/nvim")

    currentTab = nvim.api.get_current_tabpage()
    allTabs = nvim.api.list_tabpages()
    for tab in allTabs:
        if tab != currentTab:
            nvim.api.tabpage_close(tab)

    win = nvim.api.get_current_win()
    prevBuf = nvim.api.get_current_buf()

    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, textLines)

    nvim.api.buf_set_option(buf, "bufhidden", "hide")
    nvim.api.buf_set_option(buf, "modifiable", False)
    nvim.api.buf_set_option(buf, "readonly", True)
    nvim.api.win_set_buf(win, buf)
    nvim.api.win_set_option(win, "wrap", True)
    nvim.api.win_set_option(win, "number", False)
    nvim.api.win_set_option(win, "relativenumber", False)
    nvim.api.win_set_option(win, "cursorline", False)
    nvim.api.win_set_option(win, "signcolumn", "no")
    nvim.api.buf_clear_namespace(buf, 0, 0, -1)

    nvim.exec_lua("vim.g.user_entered = false")

    luaCode = """
    vim.g.prev_buf = ...
    function CloseMessageBuffer()
      vim.g.user_entered = true
      local bufnr = vim.api.nvim_get_current_buf()
      local prev_buf = vim.g.prev_buf
      if vim.api.nvim_buf_is_valid(prev_buf) then
        local win = vim.api.nvim_get_current_win()
        vim.api.nvim_win_set_buf(win, prev_buf)
      else
        local placeholder_buf = vim.api.nvim_create_buf(false, true)
        vim.api.nvim_buf_set_name(placeholder_buf, "[No Name]")
        local win = vim.api.nvim_get_current_win()
        vim.api.nvim_win_set_buf(win, placeholder_buf)
      end
      if vim.api.nvim_buf_is_valid(bufnr) then
        vim.api.nvim_buf_delete(bufnr, {force=true})
      end
    end
    """
    nvim.exec_lua(luaCode, prevBuf)

    nvim.api.buf_set_keymap(
        buf,
        "n",
        "<CR>",
        ":lua CloseMessageBuffer()<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )

    while True:
        entered = nvim.exec_lua("return vim.g.user_entered")
        if entered:
            break
        time.sleep(0.1)


def TimerWithRemindersAndPopup(seconds):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    nvim.exec_lua("vim.g.finish_timer = false")

    nvim.command("command! Finish lua vim.g.finish_timer = true")

    reminders = sorted(
        set(
            [
                seconds // 2,
                seconds // 3,
                seconds // 4,
                seconds // 5,
                300,
                180,
                120,
                60,
            ]
        ),
        reverse=True,
    )
    reminders = [r for r in reminders if 3 < r < seconds]

    def ShowPopup(lines):
        """Create a floating popup with given lines of text."""
        buf = nvim.api.create_buf(False, True)
        nvim.api.buf_set_lines(buf, 0, -1, False, lines)

        width = max(len(line) for line in lines) + 4 if lines else 10
        height = len(lines) if lines else 1
        screenWidth = nvim.api.get_option("columns")
        screenHeight = nvim.api.get_option("lines")

        row = (screenHeight - height) // 2
        col = (screenWidth - width) // 2

        opts = {
            "relative": "editor",
            "width": width,
            "height": height,
            "row": row,
            "col": col,
            "style": "minimal",
            "border": "double",
        }

        win = nvim.api.open_win(buf, True, opts)
        return win, buf

    def ClosePopup(win):
        """Safely close popup window if valid."""
        if win and nvim.api.win_is_valid(win):
            nvim.api.win_close(win, True)

    remaining = seconds
    lastTime = time.time()
    reminderIndex = 0
    popupWin = None
    popupBuf = None
    popupStartTime = None

    while remaining > 0:
        now = time.time()
        elapsed = now - lastTime
        lastTime = now
        remaining -= elapsed

        if remaining <= 0:
            break

        finish = nvim.exec_lua("return vim.g.finish_timer")
        if finish:
            print(
                f"Timer finished early by ':Finish' command with {int(remaining)} seconds left"
            )
            break

        if popupWin and popupStartTime and (now - popupStartTime > 3):
            ClosePopup(popupWin)
            popupWin = None
            popupBuf = None
            popupStartTime = None

        if reminderIndex < len(reminders) and remaining <= reminders[reminderIndex]:
            if popupWin:
                ClosePopup(popupWin)
                popupWin = None
                popupBuf = None
                popupStartTime = None

            reminderMsg = [
                f"Reminder: {int(reminders[reminderIndex])} seconds remaining!"
            ]
            popupWin, popupBuf = ShowPopup(reminderMsg)
            popupStartTime = now
            reminderIndex += 1

        elif 15 >= remaining > 3:
            timerText = [f"Timer: {int(remaining)} seconds remaining"]
            if not popupWin:
                popupWin, popupBuf = ShowPopup(timerText)
                popupStartTime = now
            else:
                nvim.api.buf_set_lines(popupBuf, 0, -1, False, timerText)
                popupStartTime = now

        elif 3 >= remaining > 0:
            reminderMsg = [f"*** LAST {int(remaining)} SECONDS ***"]
            if not popupWin:
                popupWin, popupBuf = ShowPopup(reminderMsg)
                popupStartTime = now
            else:
                nvim.api.buf_set_lines(popupBuf, 0, -1, False, reminderMsg)
                popupStartTime = now

        else:
            if popupWin and not popupStartTime:
                ClosePopup(popupWin)
                popupWin = None
                popupBuf = None

        time.sleep(0.1)

    if popupWin:
        ClosePopup(popupWin)
    SaveAllFiles()
    if remaining > 0 and finish:
        return int(remaining)
    else:
        print("Timer completed")
        return 0


def SaveAllFiles():
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    nvim.command("wall")


def SetupIdeaCommand(title, description):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    # Escape quotes to avoid Lua syntax errors
    titleEscaped = title.replace('"', '\\"')
    descriptionEscaped = description.replace('"', '\\"')

    luaCode = f'''
    function ShowIdea()
        local buf = vim.api.nvim_create_buf(false, true)  -- scratch buffer
        local lines = {{
            "{titleEscaped}",
            "",
            "{descriptionEscaped}"
        }}
        vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)

        local width = 0
        for _, line in ipairs(lines) do
            if #line > width then
                width = #line
            end
        end
        local height = #lines

        local opts = {{
            relative = "editor",
            width = width + 4,
            height = height + 2,
            row = math.floor((vim.o.lines - height) / 2),
            col = math.floor((vim.o.columns - width) / 2),
            style = "minimal",
            border = "rounded",
        }}

        local win = vim.api.nvim_open_win(buf, true, opts)

        -- Close window on pressing q or <Esc>
        vim.api.nvim_buf_set_keymap(buf, "n", "q", ":close<CR>", {{nowait=true, noremap=true, silent=true}})
        vim.api.nvim_buf_set_keymap(buf, "n", "<Esc>", ":close<CR>", {{nowait=true, noremap=true, silent=true}})
    end
    '''

    # Define ShowIdea() as Lua
    nvim.exec_lua(luaCode)

    # Define the Vim user command :Idea in Vimscript
    nvim.command("command! Idea lua ShowIdea()")


def FloatingInputPrompt(prompt_text_lines, height=5, width=50):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    # Create a scratch buffer for input (listed=False, scratch=True)
    buf = nvim.api.create_buf(False, True)

    # Compose initial lines: prompt + empty input lines
    # For example, prompt lines first, then one empty line for input
    lines = prompt_text_lines + [""] * (height - len(prompt_text_lines))
    nvim.api.buf_set_lines(buf, 0, -1, False, lines)

    # Calculate window position centered on screen
    screen_width = nvim.api.get_option("columns")
    screen_height = nvim.api.get_option("lines")
    row = (screen_height - height) // 2
    col = (screen_width - width) // 2

    opts = {
        "relative": "editor",
        "width": width,
        "height": height,
        "row": row,
        "col": col,
        "style": "minimal",
        "border": "rounded",
    }

    # Open floating window with the buffer, make it focused for user input
    win = nvim.api.open_win(buf, True, opts)

    # Set buffer options to allow insert mode (modifiable, not readonly)
    nvim.api.buf_set_option(buf, "modifiable", True)
    nvim.api.buf_set_option(buf, "bufhidden", "wipe")

    # Put cursor on the first empty line (after prompt)
    nvim.api.win_set_cursor(win, (len(prompt_text_lines) + 1, 0))

    # Define keymap to confirm input with <CR> (Enter)
    # It will set a global var to signal done and exit insert mode
    nvim.api.buf_set_keymap(
        buf,
        "i",
        "<CR>",
        "<Esc>:lua vim.g.input_done = true<CR>",
        {"nowait": True, "noremap": True, "silent": True},
    )

    # Initialize flag for input done
    nvim.exec_lua("vim.g.input_done = false")

    # Enter insert mode so user can type immediately
    nvim.command("startinsert")

    # Wait loop until user confirms (presses Enter)
    while not nvim.exec_lua("return vim.g.input_done"):
        time.sleep(0.1)

    # Get buffer lines as user input (skip prompt lines)
    input_lines = nvim.api.buf_get_lines(buf, len(prompt_text_lines), -1, False)

    # Close floating window
    nvim.api.win_close(win, True)

    # Return entered input as list of lines or join as single string if you prefer
    return input_lines


# Example usage:
if __name__ == "__main__":
    prompt = ["Please enter your text below and press Enter when done:"]
    user_input = FloatingInputPrompt(prompt)
    print("User entered:")
    print("\n".join(user_input))
