import csv
import ipywidgets as widgets
from traitlets import Dict, Unicode

@widgets.register
class Viewer(widgets.DOMWidget):
    """SCDG viewer  as a Jupyter widget.
    """
    _view_name = Unicode('ScdgViewerView').tag(sync=True)
    _model_name = Unicode('ScdgViewerModel').tag(sync=True)
    _view_module = Unicode('scdg-viewer').tag(sync=True)
    _model_module = Unicode('scdg-viewer').tag(sync=True)
    _view_module_version = Unicode('^1.0').tag(sync=True)
    _model_module_version = Unicode('^1.0').tag(sync=True)
    _model_data = Dict().tag(sync=True)
    _nodes_labels = []
    _nodes_without_label = []
    _edges_labels = []
    _edges_without_label = []
    
    def get_edge_label(self, hash):
        """ Get human-readable edge label corresponding to the hash.
        Return hash if the association file has not been loaded or if hash has not been found.

        Keyword arguments:
        hash -- edge hash
        """
        if hash in self._edges_labels:
            return self._edges_labels[hash]
        else:
            if hash not in self._edges_without_label:
                self._edges_without_label.append(hash)
            return hash

    def get_node_label(self, hash):
        """ Get human-readable node label corresponding to the hash.
        Return hash if the association file has not been loaded or if hash has not been found.

        Keyword arguments:
        hash -- node hash
        """
        if hash in self._nodes_labels:
            return self._nodes_labels[hash]
        else:
            if hash not in self._nodes_without_label:
                self._nodes_without_label.append(hash)
            return hash

    def get_unknown_edge_hash(self):
        """ Return the list of edge hashes that have no label association.
        """
        return self._edges_without_label

    def get_unknown_node_hash(self):
        """ Return the list of node hashes that have no label association.
        """
        return self._nodes_without_label

    def load_data(self, input_data):
        """ Load json data to display.
        The function will convert data to be used by vis library.

        Keyword arguments:
        input_data -- json input data
        """
        formatted_data = {}
        formatted_data["nodes"] = []
        for node in input_data["graph"]["nodes"]:
            formatted_node = {'id': node[0], 'label': self.get_node_label(str(node[1])), 'group': 'function'}
            formatted_data["nodes"].append(formatted_node)
        formatted_data["edges"] = []
        for edge in input_data["graph"]["edges"]:
            formatted_edge = {'from': edge[0], 'to': edge[1], 'label': self.get_edge_label(str(edge[2]))}
            formatted_data["edges"].append(formatted_edge)
        self._model_data = formatted_data

    def load_edges_association_file(self, filename):
        """ Load csv file that associates hashes with human-readable edge labels.

        Keyword arguments:
        filename -- the file path
        """
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            self._edges_labels = {rows[1]:rows[0] for rows in reader}
    
    def load_nodes_association_file(self, filename):
        """ Load csv file that associates hashes with human-readable node labels.

        Keyword arguments:
        filename -- the file path
        """
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            self._nodes_labels = {rows[1]:rows[0] for rows in reader}
