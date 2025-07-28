import time
import pynvim
import os
import threading


def drawFloatingWindowWithTimer(text_lines, timeout_sec):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, text_lines)

    width = max(len(line) for line in text_lines) + 2 if text_lines else 10
    height = len(text_lines) if text_lines else 1

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

    nvim.call("timer_start", int(timeout_sec * 1000), "ClosePopupWrapper")


def displayFullscreenTextWithTimer(text_lines, timeout_sec):
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, text_lines)
    width = max(len(line) for line in text_lines) + 2 if text_lines else 10
    height = len(text_lines) if text_lines else 1
    screen_width = nvim.api.get_option("columns")
    screen_height = nvim.api.get_option("lines")
    opts = {
        "relative": "editor",
        "width": screen_width,
        "height": screen_height,
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
    nvim.call("timer_start", int(timeout_sec * 1000), "ClosePopupWrapper")


def openFileInSingleTab(file_path):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    current_tab = nvim.api.get_current_tabpage()
    for tab in nvim.api.list_tabpages():
        if tab != current_tab:
            nvim.api.tabpage_close(tab, True)

    nvim.command(f"edit {file_path}")

    abs_path = os.path.abspath(file_path)
    directory = os.path.dirname(abs_path)
    nvim.command(f"cd {directory}")

    cur_buf = nvim.api.get_current_buf()
    for b in nvim.api.list_bufs():
        if b != cur_buf:
            try:
                nvim.api.buf_delete(b, {"force": True})
            except Exception:
                pass

    # Set window options to enable line numbers, relative line numbers, and sign column
    cur_win = nvim.api.get_current_win()
    nvim.api.win_set_option(cur_win, "number", True)
    nvim.api.win_set_option(cur_win, "relativenumber", True)
    nvim.api.win_set_option(cur_win, "signcolumn", "yes")


def fullscreenCountdownWithText(text, seconds):
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    buf = nvim.api.create_buf(False, True)
    screen_width = nvim.api.get_option("columns")
    screen_height = nvim.api.get_option("lines")
    opts = {
        "relative": "editor",
        "width": screen_width,
        "height": screen_height,
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
        text_lines = str(text).splitlines()
        lines_to_set = text_lines + [f"Countdown: {remaining}"]
        nvim.api.buf_set_lines(buf, 0, -1, False, lines_to_set)
        if nvim.exec_lua("return vim.g.countdown_break"):
            break
        time.sleep(1)
    nvim.api.win_close(win, True)
    return nvim.exec_lua("return vim.g.countdown_break")


def displayTextWait(text_lines):
    if isinstance(text_lines, str):
        text_lines = text_lines.splitlines() or [text_lines]
    elif isinstance(text_lines, (list, tuple)):
        text_lines = [str(line) for line in text_lines]
    else:
        raise TypeError("text_lines must be a string or list/tuple of strings")

    nvim = pynvim.attach("socket", path="/tmp/nvim")

    current_tab = nvim.api.get_current_tabpage()
    all_tabs = nvim.api.list_tabpages()
    for tab in all_tabs:
        if tab != current_tab:
            nvim.api.tabpage_close(tab)

    win = nvim.api.get_current_win()
    prev_buf = nvim.api.get_current_buf()

    buf = nvim.api.create_buf(False, True)
    nvim.api.buf_set_lines(buf, 0, -1, False, text_lines)

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

    lua_code = """
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
    nvim.exec_lua(lua_code, prev_buf)

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


def timer_with_reminders_and_popup(seconds):
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

    def show_popup(lines):
        """Create a floating popup with given lines of text."""
        buf = nvim.api.create_buf(False, True)
        nvim.api.buf_set_lines(buf, 0, -1, False, lines)

        width = max(len(line) for line in lines) + 4 if lines else 10
        height = len(lines) if lines else 1
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
            "border": "double",
        }

        win = nvim.api.open_win(buf, True, opts)
        return win, buf

    def close_popup(win):
        """Safely close popup window if valid."""
        if win and nvim.api.win_is_valid(win):
            nvim.api.win_close(win, True)

    remaining = seconds
    last_time = time.time()
    reminder_index = 0
    popup_win = None
    popup_buf = None
    popup_start_time = None

    while remaining > 0:
        now = time.time()
        elapsed = now - last_time
        last_time = now
        remaining -= elapsed

        if remaining <= 0:
            break

        finish = nvim.exec_lua("return vim.g.finish_timer")
        if finish:
            print(
                f"Timer finished early by ':Finish' command with {int(remaining)} seconds left"
            )
            break

        if popup_win and popup_start_time and (now - popup_start_time > 3):
            close_popup(popup_win)
            popup_win = None
            popup_buf = None
            popup_start_time = None

        if reminder_index < len(reminders) and remaining <= reminders[reminder_index]:
            if popup_win:
                close_popup(popup_win)
                popup_win = None
                popup_buf = None
                popup_start_time = None

            reminder_msg = [
                f"Reminder: {int(reminders[reminder_index])} seconds remaining!"
            ]
            popup_win, popup_buf = show_popup(reminder_msg)
            popup_start_time = now
            reminder_index += 1

        elif 15 >= remaining > 3:
            timer_text = [f"Timer: {int(remaining)} seconds remaining"]
            if not popup_win:
                popup_win, popup_buf = show_popup(timer_text)
                popup_start_time = now
            else:
                nvim.api.buf_set_lines(popup_buf, 0, -1, False, timer_text)
                popup_start_time = now

        elif 3 >= remaining > 0:
            reminder_msg = [f"*** LAST {int(remaining)} SECONDS ***"]
            if not popup_win:
                popup_win, popup_buf = show_popup(reminder_msg)
                popup_start_time = now
            else:
                nvim.api.buf_set_lines(popup_buf, 0, -1, False, reminder_msg)
                popup_start_time = now

        else:
            if popup_win and not popup_start_time:
                close_popup(popup_win)
                popup_win = None
                popup_buf = None

        time.sleep(0.1)

    if popup_win:
        close_popup(popup_win)
    save_all_files()
    if remaining > 0 and finish:
        return int(remaining)
    else:
        print("Timer completed")
        return 0


def save_all_files():
    nvim = pynvim.attach("socket", path="/tmp/nvim")
    nvim.command("wall")


def setup_idea_command(title, description):
    nvim = pynvim.attach("socket", path="/tmp/nvim")

    # Escape quotes to avoid Lua syntax errors
    title_escaped = title.replace('"', '\\"')
    description_escaped = description.replace('"', '\\"')

    lua_code = f'''
    function ShowIdea()
        local buf = vim.api.nvim_create_buf(false, true)  -- scratch buffer
        local lines = {{
            "{title_escaped}",
            "",
            "{description_escaped}"
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
    nvim.exec_lua(lua_code)

    # Define the Vim user command :Idea in Vimscript
    nvim.command("command! Idea lua ShowIdea()")


if __name__ == "__main__":
    setup_idea_command("title", "description")
