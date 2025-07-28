local M = {}

local function is_nvim_listening()
	local socket_path = "/tmp/nvim"
	local stat = vim.loop.fs_stat(socket_path)
	return stat ~= nil
end

function M.idealab_command()
	if not is_nvim_listening() then
		vim.api.nvim_echo({ { "Please start Neovim with 'nvim --listen /tmp/nvim' first.", "ErrorMsg" } }, true, {})
	else
		vim.api.nvim_echo(
			{ { "Neovim is listening on /tmp/nvim. :MicroSprintLab command activated.", "InfoMsg" } },
			true,
			{}
		)

		-- Start the Python script asynchronously
		vim.fn.jobstart({ "python3", vim.fn.expand("~") .. "/Documents/MicroSprintLab/main.py" }, {
			stdout_buffered = true,
			on_stdout = function(_, data)
				if data then
					for _, line in ipairs(data) do
						if line ~= "" then
							vim.api.nvim_echo({ { line, "None" } }, false, {})
						end
					end
				end
			end,
			on_stderr = function(_, data)
				if data then
					for _, line in ipairs(data) do
						if line ~= "" then
							vim.api.nvim_echo({ { "Error: " .. line, "ErrorMsg" } }, false, {})
						end
					end
				end
			end,
			on_exit = function(_, code)
				vim.api.nvim_echo({ { "Python script exited with code " .. code, "WarningMsg" } }, false, {})
			end,
		})
	end
end

function M.setup()
	vim.api.nvim_create_user_command("MicroSprintLab", function()
		M.idealab_command()
	end, {})
end

return M
