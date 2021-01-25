"""Base of stopwords utilized."""

import nltk
import pickle


local = r'C:\Users\Usuário\Projects\monografia\dados\data_final'

stopwords_pt = ['a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo',
                'alguém', 'algum', 'alguma', 'algumas', 'alguns', 'ali',
                'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante',
                'antes', 'ao', 'aos', 'apenas', 'apoio', 'após', 'aquela',
                'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área',
                'as', 'às', 'assim', 'até', 'atrás', 'através', 'baixo',
                'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve',
                'cá', 'catorze', 'cedo', 'cento', 'certamente',
                'certeza', 'cima', 'cinco', 'coisa', 'coisas', 'com', 'como',
                'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão',
                'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'das',
                'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais',
                'dentro', 'depois', 'desde', 'dessa', 'dessas', 'desse',
                'desses', 'desta', 'destas', 'deste', 'destes', 'deve',
                'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria',
                'deveriam', 'devia', 'deviam', 'dez', 'dezanove',
                'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso',
                'disto', 'dito', 'diz', 'dizem', 'dizer', 'do', 'dois', 'dos',
                'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele',
                'eles', 'em', 'embora', 'enquanto', 'entre', 'era', 'eram',
                'éramos', 'és', 'essa', 'essas', 'esse', 'esses', 'esta',
                'está', 'estamos', 'estão', 'estar', 'estas', 'estás',
                'estava', 'estavam', 'estávamos', 'este', 'esteja', 'estejam',
                'estejamos', 'estes', 'esteve', 'estive', 'estivemos',
                'estiver', 'estivera', 'estiveram', 'estivéramos',
                'estiverem', 'estivermos', 'estivesse', 'estivessem',
                'estivéssemos', 'estiveste', 'estivestes', 'estou',
                'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz',
                'fazeis', 'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes',
                'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim', 'final',
                'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem',
                'forma', 'formos', 'fosse', 'fossem', 'fôssemos', 'foste',
                'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há',
                'haja', 'hajam', 'hajamos', 'hão', 'havemos', 'havia', 'hei',
                'hoje', 'houve', 'houvemos', 'houver',
                'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão',
                'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam',
                'houveríamos', 'houvermos', 'houvesse', 'houvessem',
                'houvéssemos', 'isso', 'isto', 'já', 'la', 'lá', 'lado',
                'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar',
                'maior', 'maioria', 'mais', 'mal', 'mas', 'máximo', 'me',
                'meio', 'menor', 'menos', 'mês', 'meses', 'mesma', 'mesmas',
                'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas',
                'momento', 'muita', 'muitas', 'muito', 'muitos', 'na', 'nada',
                'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas',
                'nem', 'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse',
                'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ninguém',
                'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa',
                'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 'novo',
                'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra',
                'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde',
                'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro',
                'outros', 'para', 'parece', 'parte', 'partir', 'paucas',
                'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas',
                'pequeno', 'pequenos', 'per', 'perante', 'perto', 'pode',
                'pude', 'pôde', 'podem', 'podendo', 'poder', 'poderia',
                'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois',
                'ponto', 'pontos', 'por', 'porém', 'porque', 'porquê',
                'posição', 'possível', 'possivelmente', 'posso', 'pouca',
                'poucas', 'pouco', 'poucos', 'primeira', 'primeiras',
                'primeiro', 'primeiros', 'própria', 'próprias', 'próprio',
                'próprios', 'próxima', 'próximas', 'próximo', 'próximos',
                'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando',
                'quanto', 'quantos', 'quarta', 'quarto', 'quatro', 'que',
                'quê', 'quem', 'quer', 'quereis', 'querem', 'queremas',
                'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze',
                'relação', 'sabe', 'sabem', 'são', 'se', 'segunda', 'segundo',
                'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre',
                'sendo', 'ser', 'será', 'serão', 'serei', 'seremos', 'seria',
                'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu',
                'seus', 'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema',
                'só', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua', 'suas',
                'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas',
                'tanto', 'tão', 'tarde', 'te', 'tem', 'tém', 'têm', 'temos',
                'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho',
                'tens', 'ter', 'terá', 'terão', 'terceira', 'terceiro',
                'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu',
                'teus', 'teve', 'ti', 'tido', 'tinha', 'tinham', 'tínhamos',
                'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tivéramos',
                'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos',
                'tiveste', 'tivestes', 'toda', 'todas', 'todavia', 'todo',
                'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas',
                'tudo', 'última', 'últimas', 'último', 'últimos', 'um', 'uma',
                'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm',
                'vendo', 'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo',
                'vinte', 'vir', 'você', 'vocês', 'vos', 'vós', 'vossa',
                'zero', '(', ')', '-', '_', 'b', 'c',
                'x', 'y', 'a', 'w', 'h', 't', 'yt']

nltk.download('stopwords')
stopwords_nltk = nltk.corpus.stopwords.words('portuguese')
stopwords_pt = list(set(stopwords_pt.extend(stopwords_nltk)))

stopwords_en = ["a", "about", "above", "after", "again", "against", "ain",
                "all", "am", "an", "and", "any", "are", "aren", "aren't", "as",
                "at", "be", "because", "been", "before", "being", "below",
                "between", "both", "but", "by", "can", "couldn", "couldn't",
                "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't",
                "doing", "don", "don't", "down", "during", "each", "few",
                "for", "from", "further", "had", "hadn", "hadn't", "has",
                "hasn", "hasn't", "have", "haven", "haven't", "having", "he",
                "her", "here", "hers", "herself", "him", "himself", "his",
                "how", "i", "if", "in", "into", "is", "isn", "isn't", "it",
                "it's", "its", "itself", "just", "ll", "m", "ma", "me",
                "mightn", "mightn't", "more", "most", "mustn", "mustn't",
                "my", "myself", "needn", "needn't", "no", "nor", "not", "now",
                "o", "of", "off", "on", "once", "only", "or", "other", "our",
                "ours", "ourselves", "out", "over", "own", "re", "s", "same",
                "shan", "shan't", "she", "she's", "should", "should've",
                "shouldn", "shouldn't", "so", "some", "such", "t", "than",
                "that", "that'll", "the", "their", "theirs", "them",
                "themselves", "then", "there", "these", "they", "this",
                "those", "through", "to", "too", "under", "until", "up", "ve",
                "very", "was", "wasn", "wasn't", "we", "were", "weren",
                "weren't", "what", "when", "where", "which", "while", "who",
                "whom", "why", "will", "with", "won", "won't", "wouldn",
                "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've",
                "your", "yours", "yourself", "yourselves", "could", "he'd",
                "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm",
                "i've", "let's", "ought", "she'd", "she'll", "that's",
                "there's", "they'd", "they'll", "they're", "they've", "we'd",
                "we'll", "we're", "we've", "what's", "when's", "where's",
                "who's", "why's", "would", "able", "abst", "accordance",
                "according", "accordingly", "across", "act", "actually",
                "added", "adj", "affected", "affecting", "affects",
                "afterwards", "ah", "almost", "alone", "along", "already",
                "also", "although", "always", "among", "amongst", "announce",
                "another", "anybody", "anyhow", "anymore", "anyone",
                "anything", "anyway", "anyways", "anywhere", "apparently",
                "approximately", "arent", "arise", "around", "aside", "ask",
                "asking", "auth", "available", "away", "awfully", "b", "back",
                "became", "become", "becomes", "becoming", "beforehand",
                "begin", "beginning", "beginnings", "begins", "behind",
                "believe", "beside", "besides", "beyond", "biol", "brief",
                "briefly", "c", "ca", "came", "cannot", "can't", "cause",
                "causes", "certain", "certainly", "co", "com", "come", "comes",
                "contain", "containing", "contains", "couldnt", "date",
                "different", "done", "downwards", "due", "e", "ed", "edu",
                "effect", "eg", "eight", "eighty", "either", "else",
                "elsewhere", "end", "ending", "enough", "especially", "et",
                "etc", "even", "ever", "every", "everybody", "everyone",
                "everything", "everywhere", "ex", "except", "f", "far", "ff",
                "fifth", "first", "five", "fix", "followed", "following",
                "follows", "former", "formerly", "forth", "found", "four",
                "furthermore", "g", "gave", "get", "gets", "getting", "give",
                "given", "gives", "giving", "go", "goes", "gone", "got",
                "gotten", "h", "happens", "hardly", "hed", "hence",
                "hereafter", "hereby", "herein", "heres", "hereupon", "hes",
                "hi", "hid", "hither", "home", "howbeit", "however", "hundred",
                "id", "ie", "im", "immediate", "immediately", "importance",
                "important", "inc", "indeed", "index", "information",
                "instead", "invention", "inward", "itd", "it'll", "j", "k",
                "keep", "keeps", "kept", "kg", "km", "know", "known", "knows",
                "l", "largely", "last", "lately", "later", "latter",
                "latterly", "least", "less", "lest", "let", "lets", "like",
                "liked", "likely", "line", "little", "ll", "look", "looking",
                "looks", "ltd", "made", "mainly", "make", "makes", "many",
                "may", "maybe", "mean", "means", "meantime", "meanwhile",
                "merely", "mg", "might", "million", "miss", "ml", "moreover",
                "mostly", "mr", "mrs", "much", "mug", "must", "n", "na",
                "name", "namely", "nay", "nd", "near", "nearly", "necessarily",
                "necessary", "need", "needs", "neither", "never",
                "nevertheless", "new", "next", "nine", "ninety", "nobody",
                "non", "none", "nonetheless", "noone", "normally", "nos",
                "noted", "nothing", "nowhere", "obtain", "obtained",
                "obviously", "often", "oh", "ok", "okay", "old", "omitted",
                "one", "ones", "onto", "ord", "others", "otherwise", "outside",
                "overall", "owing", "p", "page", "pages", "part", "particular",
                "particularly", "past", "per", "perhaps", "placed", "please",
                "plus", "poorly", "possible", "possibly", "potentially", "pp",
                "predominantly", "present", "previously", "primarily",
                "probably", "promptly", "proud", "provides", "put", "q", "que",
                "quickly", "quite", "qv", "r", "ran", "rather", "rd",
                "readily", "really", "recent", "recently", "ref", "refs",
                "regarding", "regardless", "regards", "related", "relatively",
                "research", "respectively", "resulted", "resulting", "results",
                "right", "run", "said", "saw", "say", "saying", "says", "sec",
                "section", "see", "seeing", "seem", "seemed", "seeming",
                "seems", "seen", "self", "selves", "sent", "seven", "several",
                "shall", "shed", "shes", "show", "showed", "shown", "showns",
                "shows", "significant", "significantly", "similar",
                "similarly", "since", "six", "slightly", "somebody", "somehow",
                "someone", "somethan", "something", "sometime", "sometimes",
                "somewhat", "somewhere", "soon", "sorry", "specifically",
                "specified", "specify", "specifying", "still", "stop",
                "strongly", "sub", "substantially", "successfully",
                "sufficiently", "suggest", "sup", "sure", "take", "taken",
                "taking", "tell", "tends", "th", "thank", "thanks", "thanx",
                "thats", "that've", "thence", "thereafter", "thereby",
                "thered", "therefore", "therein", "there'll", "thereof",
                "therere", "theres", "thereto", "thereupon", "there've",
                "theyd", "theyre", "think", "thou", "though", "thoughh",
                "throug", "throughout", "thru", "thus", "til",
                "tip", "together", "took", "toward", "towards", "tried",
                "tries", "truly", "try", "trying", "ts", "twice", "two", "u",
                "un", "unfortunately", "unless", "unlike", "unlikely", "unto",
                "upon", "ups", "us", "use",
                "uses", "using", "usually", "v", "various",
                "'ve", "via", "viz", "vol", "vols", "vs", "w",
                "wasnt", "way", "wed", "welcome", "went", "werent", "whatever",
                "what'll", "whats", "whence", "whenever", "whereafter",
                "whereas", "whereby", "wherein", "wheres", "whereupon",
                "wherever", "whether", "whim", "whither", "whod", "whoever",
                "whole", "who'll", "whomever", "whos", "whose", "widely",
                "willing", "wish", "within", "without", "wont", "wouldnt",
                "www", "x", "yes", "yet", "youd", "youre", "z", "zero", "a's",
                "ain't", "allow", "allows", "apart",
                "appear", "appreciate", "appropriate",
                "better", "cant",
                "consequently", "consider", "considering", "corresponding",
                "course", "currently", "definitely", "despite",
                "entirely", "exactly", "example", "going", "greetings",
                "help", "hopefully", "ignored", "inasmuch", "indicate",
                "indicated", "indicates", "inner", "insofar", "it'd", "keep",
                "keeps", "novel", "presumably", "reasonably", "second",
                "secondly", "sensible", "serious", "seriously", "sure", "t's",
                "third", "thorough", "thoroughly", "three", "well", "wonder",
                "(", ")", "_", "-", ""]

# Attention: we decided to merge the stopwords lists for a simple reason:
# even the papers in portuguese have a lot of english term (besides the
# abstraction part of a article). This can happen as well in english papers
# (with the "resumo" part).

stopwords_total = stopwords_en + stopwords_pt

with open(f'{local}/stopwords_total.pkl', 'wb') as f:
    pickle.dump(stopwords_total, f)

stopwords_total.append('modelo')
stopwords_total.append('resultado')
stopwords_total.append('como')
stopwords_total.append('para')
stopwords_total.append('model')
stopwords_total.append('economia')
stopwords_total.append('economics')
stopwords_total.append('variável')
stopwords_total.append('variable')
stopwords_total.append('variable')
stopwords_total.append('variáveis')
stopwords_total.append('estimate')
stopwords_total.append('produto')
stopwords_total.append('variável')
# Those below are used when Stemming was already done
stopwords_total.append('produt')
stopwords_total.append('tax')
stopwords_total.append('variav')
stopwords_total.append('pais')
stopwords_total.append('rate')
stopwords_total.append('taxa')
stopwords_total.append('cid')
stopwords_total.append('cidcidcidcidcidcidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcidcid')
stopwords_total.append('cidcidcidcidcidcid')
stopwords_total.append('cidcidcidcid')
stopwords_total.append('cidcidcid')
stopwords_total.append('cidcid')
stopwords_total.append('cidcidmencidhjkcidcid')
stopwords_total.append('cidcidt')
stopwords_total.append(""""cidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcid
                       cidcid""")
stopwords_total.append("""cidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcid
                       cidcidcid""")
stopwords_total.append("""cidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcid
                       cidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcid
                       cidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcidcid
                       cidcidcidcid""")
pickle.dump(stopwords_total, open(f'{local}\\stopwords_total.pkl', 'wb'))
