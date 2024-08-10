# i3 Workspace Manager

## Description

The `i3-workspace-manager` is a set of tools designed to manage and restore i3 window manager workspaces efficiently. This tool allows you to capture the current state of all your i3 workspaces, including window layouts and running applications, and restore them with ease. Ideal for users who want to maintain a consistent workflow across reboots or sessions.

## Features

- **Capture Workspace Layouts**: Automatically save the layout and the list of running applications for each workspace.
- **Restore Layouts**: Restore saved layouts and start the applications in the specified workspaces.
- **Configuration File**: Use a JSON configuration file to manage workspace settings and applications.
- **Automation**: Easily integrate with your i3 config to restore layouts automatically on login.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/i3-workspace-manager.git
    cd i3-workspace-manager
    ```

2. **Make Scripts Executable**:

    ```bash
    chmod +x capture_i3_layouts.py
    chmod +x i3_workspace_manager.py
    ```

3. **Install Dependencies**:

    Ensure you have Python 3 and `i3` installed. The script uses `i3-msg` to interact with the i3 window manager.

## Usage

### Capturing Layouts

Run the following command to capture the layout of all workspaces and save them to the `~/layouts` directory:

```bash
python3 capture_i3_layouts.py
```

This will create layout files and a configuration JSON file in the `~/layouts` directory.

### Restoring Layouts

To restore the saved layouts and start applications, use:

```bash
python3 i3_workspace_manager.py restore
```

You can integrate this command into your i3 configuration file to automate the restore process on login.

## Configuration

Edit the `i3_layout_config.json` file located in the `~/layouts` directory to adjust workspace settings and application commands as needed.

### Example Configuration

```json
{
    "workspaces": {
        "1": {
            "layout": "~/layouts/workspace1.json",
            "apps": ["alacritty", "firefox"]
        },
        "2": {
            "layout": "~/layouts/workspace2.json",
            "apps": ["thunar", "code"]
        }
        // Add more workspaces as needed
    }
}
```

## Integration with i3

To automatically restore your workspace layouts on login, add the following line to your i3 configuration file (`~/.config/i3/config` or `~/.i3/config`):

```bash
exec --no-startup-id python3 ~/i3-workspace-manager/capture_i3_layouts.py && python3 ~/i3-workspace-manager/i3_workspace_manager.py restore
```

## Contribution

Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please reach out to [your-email@example.com](mailto:rwc.webster@gmail.com).
