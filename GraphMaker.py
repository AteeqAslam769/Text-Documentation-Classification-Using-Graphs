~import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from collections import Counter

def create_gui():
    
    k=5
    def update_k():
        k = int(k_value.get())
        
    def generate_data():
        folder_paths = [
        r"FashionAndBeauty",
        r"HealthAndFitness",
        r"ScienceAndEducation"
        ]
        start_file = int(start_file_entry.get())
        end_file = int(end_file_entry.get())
        process_data(folder_paths, start_file, end_file)
        # Call your data generation function with start_file and end_file values

    distances = []
    def upload_file():
        test_file_path = filedialog.askopenfilename()
        G, pos = load_graph_from_pickle(test_file_path)
        if G is not None and pos is not None:
            plt.figure(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=12)
            plt.title("Test Graph")
            plt.show()
        else:
            print("Failed to load test graph.")
        if G is not None and pos is not None:
            train_folder_path = r"Training Data"
            for filename in os.listdir(train_folder_path):
                if filename.endswith("_train_graph.pkl"):
                    train_file_path = os.path.join(train_folder_path, filename)
                    train_G, train_pos = load_graph_from_pickle(train_file_path)
                    if train_G is not None and train_pos is not None:
                        # Extract the label from the training file path and pass it to calculate_mcs
                        train_label = filename.split("_")[0]
                        distance, label = calculate_mcs(G, train_G, train_label)
                        distances.append((distance, label))
                    else:
                        print("Failed to load training graph from:", filename)
                   
        

    def predict_class():
        nearest_neighbors = knn(distances, k)
        nearest_neighbors_lables = list()
        for neighbor_lables in nearest_neighbors:
            nearest_neighbors_lables.append(neighbor_lables[1])
        update_k()
        prediction(nearest_neighbors_lables)
        distances.clear()
        pass

    root = tk.Tk()
    root.title("Graph Data Processing")

    # Set background color
    root.configure(bg="#f0f0f0")

    # Create a frame to hold all widgets
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    k_label = ttk.Label(frame, text="Length of k:", style="Custom.TLabel")
    k_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    k_value = tk.StringVar(value="5")  # Default value for k
    k_spinbox = tk.Spinbox(frame, from_=1, to=10, textvariable=k_value, command=update_k)
    k_spinbox.grid(row=4, column=1, padx=5, pady=5)

    # Start File Entry
    start_file_label = ttk.Label(frame, text="Start file:", style="Custom.TLabel")
    start_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    start_file_entry = ttk.Entry(frame)
    start_file_entry.grid(row=0, column=1, padx=5, pady=5)

    # End File Entry
    end_file_label = ttk.Label(frame, text="End file:", style="Custom.TLabel")
    end_file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    end_file_entry = ttk.Entry(frame)
    end_file_entry.grid(row=1, column=1, padx=5, pady=5)

    # Generate Data Button
    generate_button = ttk.Button(frame, text="Generate Data", command=generate_data)
    generate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Upload File Button
    upload_button = ttk.Button(frame, text="Upload File For Classification", command=upload_file)
    upload_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Predict Class Button
    predict_button = ttk.Button(frame, text="Predict Class", command=predict_class)
    predict_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Style configuration
    style = ttk.Style()
    style.configure("Custom.TLabel", foreground="#333333", background="#f0f0f0")

    root.mainloop()


# Read tokens from a text file
def read_tokens_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tokens = file.read().split()
    return tokens


# Create a graph from tokens
def create_graph_from_tokens(tokens):
    G = nx.Graph()
    G.add_nodes_from(tokens)
    for i in range(len(tokens) - 1):
        G.add_edge(tokens[i], tokens[i + 1])
    return G


def process_folders_with_range(folder_paths, start_file_num, end_file_num):
    train_folder = os.path.join(os.getcwd(), "Training Data")
    os.makedirs(train_folder, exist_ok=True)  # Create "Training Data" folder if it doesn't exist

    test_folder = os.path.join(os.getcwd(), "Test Data")
    os.makedirs(test_folder, exist_ok=True)  # Create "Test Data" folder if it doesn't exist

    for folder_path in folder_paths:
        folder_name = os.path.basename(folder_path)  # Get the folder name for uniqueness
        
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".txt"):
                file_num = int(filename.split("blog")[1].split(".")[0])
                file_path = os.path.join(folder_path, filename)
                print("Processing:", file_path)

                # Read tokens from the file
                document_tokens = read_tokens_from_file(file_path)

                # Create graph from tokens
                G = create_graph_from_tokens(document_tokens)

                # Add space between nodes for visualization (using spring layout)
                pos = nx.spring_layout(G, k=0.5)  # Adjust the value of k for more or less space between nodes

                
                
                if start_file_num <= file_num <= end_file_num:
                    # Save training graph data with unique name
                    train_save_name = f"{folder_name}_{filename.split('.')[0]}_train_graph.pkl"
                    train_save_path = os.path.join(train_folder, train_save_name)
                    with open(train_save_path, 'wb') as f:
                        pickle.dump((G, pos), f)
                else:
                    # Save test graph data with unique name
                    test_save_name = f"{folder_name}_{filename.split('.')[0]}_test_graph.pkl"
                    test_save_path = os.path.join(test_folder, test_save_name)
                    with open(test_save_path, 'wb') as f:
                        pickle.dump((G, pos), f)
                        
def process_data(folder_paths, start_file_num, end_file_num):
    process_folders_with_range(folder_paths, start_file_num, end_file_num)


def load_graph_from_pickle(file_path):
    try:
        with open(file_path, 'rb') as f:
            graph_data = pickle.load(f)
            if isinstance(graph_data, tuple) and len(graph_data) == 2:
                G = graph_data[0]
                pos = graph_data[1]
                return G, pos
            else:
                print("Invalid data format in the pickle file.")
                return None, None
    except FileNotFoundError:
        print("File not found.")
        return None, None
    except pickle.UnpicklingError:
        print("Error while unpickling the file.")
        return None, None
    
    
def calculate_mcs(G1, G2,lable):
    # Initialize an empty graph for the common subgraph
    common_subgraph = nx.Graph()

    # Iterate through nodes in G1
    for node in G1.nodes():
        if node in G2.nodes():
            common_subgraph.add_node(node)

    # Iterate through edges in G1
    for edge in G1.edges():
        if edge[0] in common_subgraph.nodes() and edge[1] in common_subgraph.nodes():
            common_subgraph.add_edge(edge[0], edge[1])

    # Calculate MCS size and maximum size
    mcs_size = len(common_subgraph.nodes()) + len(common_subgraph.edges())
    max_size = max(len(G1.nodes()) + len(G1.edges()), len(G2.nodes()) + len(G2.edges()))

    # Calculate MCS score
    mcs_score = 1 - mcs_size / max_size
    return mcs_score, lable


def knn(distances, k):
    # Sort the distances based on the MCS score (distance)
    distances.sort()

    # Select the top k samples with the smallest distances
    nearest_neighbors = distances[:k]

    return nearest_neighbors


def prediction(neighbor_lables):
    label_counts = Counter(neighbor_lables)
    predicted_class = max(label_counts, key=label_counts.get)

    print("Predicted class:", predicted_class)
    
    
    
def main():
    create_gui()
    

if __name__ == "__main__":
    main()