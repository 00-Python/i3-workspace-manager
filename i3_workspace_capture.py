import os
import subprocess
import json

# Function to run a shell command and capture its output
def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode().strip(), result.stderr.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e.stderr.decode().strip()}")
        return '', e.stderr.decode().strip()

# Function to capture and save workspace layouts
def capture_layouts(save_dir):
    # Create directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Get the list of workspaces
    workspaces_json, error = run_cmd("i3-msg -t get_workspaces")
    if error or not workspaces_json:
        print("Failed to get workspaces.")
        return
    
    try:
        workspaces = json.loads(workspaces_json)
    except json.JSONDecodeError as e:
        print(f"Failed to parse workspaces JSON: {e}")
        return

    config = {"workspaces": {}}

    # Iterate over each workspace
    for ws in workspaces:
        workspace_num = ws['num']
        layout_file = os.path.join(save_dir, f"workspace{workspace_num}.json")

        # Save the layout for the workspace
        layout_cmd = f"i3-save-tree --workspace {workspace_num}"
        layout_json, error = run_cmd(layout_cmd)
        if error or not layout_json:
            print(f"Failed to save layout for workspace {workspace_num}")
            continue
        
        # Write layout JSON to file
        try:
            with open(layout_file, 'w') as f:
                f.write(layout_json)
        except IOError as e:
            print(f"Failed to write layout to file for workspace {workspace_num}: {e}")
            continue
        
        # Get the list of windows (applications) on this workspace
        tree_json, error = run_cmd("i3-msg -t get_tree")
        if error or not tree_json:
            print(f"Failed to get tree for workspace {workspace_num}")
            continue
        
        try:
            tree = json.loads(tree_json)
        except json.JSONDecodeError as e:
            print(f"Failed to parse tree JSON for workspace {workspace_num}: {e}")
            continue

        apps = []

        def extract_apps(node):
            if 'nodes' in node:
                for subnode in node['nodes']:
                    extract_apps(subnode)
            if 'floating_nodes' in node:
                for subnode in node['floating_nodes']:
                    extract_apps(subnode)
            if 'window_properties' in node and node['window_properties']:
                if node['window_properties'].get('class'):
                    apps.append(node['window_properties']['class'])

        extract_apps(tree)

        # Add the layout and apps to the config
        config['workspaces'][str(workspace_num)] = {
            "layout": layout_file,
            "apps": apps
        }
        print(f"Captured layout and apps for workspace {workspace_num}")

    # Save the config to a JSON file
    config_file = os.path.join(save_dir, "i3_layout_config.json")
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Failed to write configuration to file: {e}")
        return
    
    print(f"Configuration saved to {config_file}")

if __name__ == "__main__":
    save_directory = os.path.expanduser("~/layouts")
    capture_layouts(save_directory)

