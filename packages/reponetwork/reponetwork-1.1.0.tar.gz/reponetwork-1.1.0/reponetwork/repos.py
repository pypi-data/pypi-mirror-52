import networkx as nx
import networkx.algorithms.isomorphism as iso
import itertools
import argparse
import dateutil
import matplotlib
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib import cm, colors

from reponetwork.GithubCrawler import GithubCrawler
from reponetwork.GitlabCrawler import GitlabCrawler


def analize_graph(g: nx.Graph, limit: int = 3, clean: bool = True, draw: bool = False, cmp_with: nx.Graph = None):
    assert isinstance(g, nx.Graph)
    assert isinstance(limit, int)
    assert cmp_with is None or isinstance(cmp_with, nx.Graph)

    def take_by_value(items, l, f=None):
        items = sorted(items, key=lambda t: t[1], reverse=True)
        if f is not None:
            items = filter(f, items)
        return [k for k, v in itertools.islice(items, 0, l)]

    labels = set()
    print('Graph analysis:')
    nodes = g.nodes(data=True)
    repos = {n for n, d in nodes if d['bipartite'] == 0}
    print('Repositories: {0}'.format(len(repos)))
    users = set(g) - repos
    print('Users: {0}'.format(len(users)))
    components = list(nx.connected_components(g))
    print('Connected components: \n{0}'.format(sum(1 for _ in components)))
    languages = {d['language'] for n, d in nodes if d['bipartite'] == 0}
    print('Languages: \n{0}'.format(languages))

    bridges = {(n1, n2): len(next((c for c in components if n1 in c), [])) for n1, n2 in nx.algorithms.bridges(g)}
    bridges = take_by_value(bridges.items(), limit)
    print('Connecting memberships: \n{0}'.format(list(bridges)))

    deg1_repos = [n for n in repos if g.degree[n] <= 1]
    print('Number of risked projects: \n{0}'.format(len(deg1_repos)))
    deg1_repos = sorted(deg1_repos, key=lambda n: -nodes[n].get('weight', 0))
    print('Most risked projects: \n{0}'.format(deg1_repos[0:limit]))

    if cmp_with:
        print('Comparing graphs...')
        nm = iso.categorical_node_match(['bipartite', 'language'], [0, '?'])
        em = iso.categorical_edge_match('relation', 'contributor')
        #are_equal = nx.is_isomorphic(g, cmp_with, node_match=nm, edge_match=em)
        are_equal = nx.could_be_isomorphic(g, cmp_with)
        print('The graphs are similar.' if are_equal else 'The graphs are not isomorphic.')

    if clean:
        repo_count = len(repos)
        components = sorted(components, key=lambda c: len(c))
        min_size = len(components[-1])/2

        for component in components:
            component_repos = repos.intersection(component)
            if len(component_repos) <= 1 or len(component) < min_size:
                repos.difference_update(component)
                users.difference_update(component)
                # g.remove_nodes_from(component)

        if len(repos) < repo_count:
            print('Excluded {0} isolated projects.'.format(repo_count - len(repos)))
            # g = nx.classes.graphviews.subgraph_view(g, filter_node=lambda n: n in repos or n in users)
            g = nx.subgraph(g, repos.union(users))

    if limit and repos:
        fork_sources = {n: d.get('fork_source') for n, d in nodes if d.get('relation') == 'fork'}
        fork_count = {n: sum(1 for k, v in fork_sources if v == n) for n in repos}
        fork_count = take_by_value(fork_count.items(), limit)
        labels.update(fork_count)
        print('Most forked projects: \n{0}'.format(fork_count))

        repo_centrality = nx.algorithms.bipartite.degree_centrality(g, repos)
        repo_centrality = take_by_value(repo_centrality.items(), limit, f=lambda t: t[0] in repos)
        labels.update(repo_centrality)
        print('Most popular projects: \n{0}'.format(repo_centrality))

        repo_centrality = nx.algorithms.bipartite.closeness_centrality(g, repos, normalized=True)
        repo_centrality = take_by_value(repo_centrality.items(), limit, f=lambda t: t[0] in repos)
        labels.update(repo_centrality)
        print('Most central projects: \n{0}'.format(repo_centrality))

        user_centrality = nx.algorithms.bipartite.degree_centrality(g, users)
        user_centrality = take_by_value(user_centrality.items(), limit, f=lambda t: t[0] in users)
        labels.update(user_centrality)
        print('Most active users: \n{0}'.format(user_centrality))

        user_languages = {u: len(set(nodes[n]['language'] for n in nx.neighbors(g, u) if nodes[n]['language']))
                          for u in users}
        user_centrality = nx.algorithms.bipartite.betweenness_centrality(g, users)
        user_centrality = take_by_value(user_centrality.items(), limit, f=lambda t: user_languages.get(t[0]) or 0 > 1)
        labels.update(user_centrality)
        print('Users connecting communities: \n{0}'.format(user_centrality))
    if draw:
        draw_communities(g, labels=list(labels))


def draw_communities(G: nx.Graph, labels=None):
    assert isinstance(G, nx.Graph)
    assert labels is None or isinstance(labels, list)

    labels = {n: n for n in labels} if labels else {}

    print('Drawing graph...')
    pos = nx.spring_layout(G)
    nodes = G.nodes(data=True)
    languages = {d['language'] for n, d in nodes if d['bipartite'] == 0}
    languages = {x: i for i, x in enumerate(languages, start=0)}
    norm = colors.Normalize(vmin=0, vmax=len(languages))
    node_list = list(G.nodes)
    color_list = ['0.3' if d['bipartite'] else cm.jet(norm(languages[d['language']])) for n, d in nodes]
    size_list = [2 if d['bipartite'] else 6 for n, d in nodes]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot([0], [0], color='0.3', label='User')
    for l, i in languages.items():
        ax.plot([0], [0], color=cm.jet(norm(i)), label=l)
    plt.title("Github repositories")
    nx.draw_networkx(G, pos=pos, nodelist=node_list, node_color=color_list, node_size=size_list,
                     with_labels=True, labels=labels, ax=ax, edge_color='0.7')
    plt.legend()
    plt.show()


def main():
    github_repo = ['https://www.github.com', 'www.github.com', 'github.com']

    parser = argparse.ArgumentParser(description='Analyze the network of code projects in a code repository.')
    parser.add_argument('-i', '--input', help='Path of a previously saved graph in GEXF format.')
    parser.add_argument('--stats', type=int, default=0, help='Specify the amount of results to display in graph analysis. '
                                                        'Use 0 to disable graph analysis.')
    parser.add_argument('--draw', dest='draw', action='store_true', help='Draw the resulting graph.')
    parser.add_argument('-s', '--source', default=github_repo[0],
                        help='The URL of the repository.')
    parser.add_argument('-u', '--user', help='The user name to use for login. '
                                             'Login is not usually required but can offer advantages.')
    parser.add_argument('-p', '--password', help='The password to use for login. '
                                                 'Login is not usually required but can offer advantages.')
    parser.add_argument('-t', '--token', help='Your private token for authentication. '
                                              'Login is not usually required but can offer advantages.')
    parser.add_argument('-l', '--limit', type=int, default=1000000,
                        help='The maximum number of repositories to include in the graph.')
    parser.add_argument('-q', '--query', help='Search the projects that match the specified text.')
    parser.add_argument('--since', type=lambda s: dateutil.parser.parse(s),
                        help='Starting date.')
    parser.add_argument('-o', '--output', help='Specify a path to save the resulting graph in GEXF format.')
    parser.add_argument('--compare', help='Path of another graph in GEXF format to compare with.')
    args = parser.parse_args()

    if args.source.lower() in github_repo:
        c = GithubCrawler(token=args.token, user=args.user, password=args.password)
    else:
        c = GitlabCrawler(args.source, token=args.token, user=args.user, password=args.password)

    g: nx.Graph = None
    g2: nx.Graph = None
    if args.input:
        g = nx.read_gexf(args.input)
        print('Loaded graph from {0}'.format(args.input))
        if args.since:
            nodes = g.nodes(data=True)
            edges = g.edges(data=True)
            g.remove_edges_from(
                [(e1, e2) for e1, e2, d in edges if 'date' in d and dateutil.parser.parse(d['date']) < args.since])
            g.remove_nodes_from(
                [n for n, d in nodes if 'date' in d and dateutil.parser.parse(d['date']) < args.since])
            print('Excluded information prior to {0}'.format(args.since))

    if args.compare:
        g2 = nx.read_gexf(args.compare)
        print('Loaded graph from {0} for comparison'.format(args.input))

    if args.query:
        print('Searching for projects matching {0}'.format(args.query))
        for g in c.find(args.query, limit=args.limit, since=args.since, previous=g):
            if args.output:
                nx.write_gexf(g, args.output)
                print('Saved to {0}'.format(args.output))
            analize_graph(g, limit=args.stats, draw=args.draw, cmp_with=g2)
    elif g:
        analize_graph(g, limit=args.stats, draw=args.draw, cmp_with=g2)
    else:
        print('Nothing to analyze')


if __name__ == "__main__":
    main()
