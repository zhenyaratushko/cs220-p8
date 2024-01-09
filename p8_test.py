#!/usr/bin/python
import os, json, math

MAX_FILE_SIZE = 300 # units - KB
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE = "text list_ordered namedtuple"  # question type when the expected answer is a list of namedtuples where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered"  # question type when the expected answer is a list of dicts where the order does matter


expected_json =    {"1": (TEXT_FORMAT_DICT, {'tt3104988': 'Crazy Rich Asians',
                                                           'nm0160840': 'Jon M. Chu',
                                                           'nm2090422': 'Constance Wu',
                                                           'nm6525901': 'Henry Golding',
                                                           'nm0000706': 'Michelle Yeoh',
                                                           'nm2110418': 'Gemma Chan',
                                                           'nm0523734': 'Lisa Lu',
                                                           'tt4846340': 'Hidden Figures',
                                                           'nm0577647': 'Theodore Melfi',
                                                           'nm0378245': 'Taraji P. Henson',
                                                           'nm0818055': 'Octavia Spencer',
                                                           'nm1847117': 'Janelle Monáe'}),
                    "2": (TEXT_FORMAT, 'Gemma Chan'),
                    "3": (TEXT_FORMAT_UNORDERED_LIST, ['Jon M. Chu',
                                                       'Constance Wu',
                                                       'Henry Golding',
                                                       'Michelle Yeoh',
                                                       'Gemma Chan',
                                                       'Lisa Lu',
                                                       'Theodore Melfi',
                                                       'Taraji P. Henson',
                                                       'Octavia Spencer',
                                                       'Janelle Monáe']),
                    "4": (TEXT_FORMAT_UNORDERED_LIST,['nm0818055']),
                    "5": (TEXT_FORMAT_LIST_DICTS_ORDERED, [{'title': 'tt3104988',
                                                            'year': 2018,
                                                            'genres': ['Comedy', 'Drama', 'Romance'],
                                                            'duration': 120,
                                                            'directors': ['nm0160840'],
                                                            'cast': ['nm2090422', 'nm6525901', 'nm0000706', 'nm2110418', 'nm0523734'],
                                                            'rating': 6.9},
                                                           {'title': 'tt4846340',
                                                            'year': 2016,
                                                            'genres': ['Biography', 'Drama', 'History'],
                                                            'duration': 127,
                                                            'directors': ['nm0577647'],
                                                            'cast': ['nm0378245', 'nm0818055', 'nm1847117'],
                                                            'rating': 7.8}]),
                    "6": (TEXT_FORMAT, 5),
                    "7": (TEXT_FORMAT, 'nm2090422'),
                    "8": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Crazy Rich Asians',
                                                      'year': 2018,
                                                      'genres': ['Comedy', 'Drama', 'Romance'],
                                                      'duration': 120,
                                                      'directors': ['Jon M. Chu'],
                                                      'cast': ['Constance Wu',
                                                      'Henry Golding',
                                                      'Michelle Yeoh',
                                                      'Gemma Chan',
                                                      'Lisa Lu'],
                                                      'rating': 6.9},
                                                     {'title': 'Hidden Figures',
                                                      'year': 2016,
                                                      'genres': ['Biography', 'Drama', 'History'],
                                                      'duration': 127,
                                                      'directors': ['Theodore Melfi'],
                                                      'cast': ['Taraji P. Henson', 'Octavia Spencer', 'Janelle Monáe'],
                                                      'rating': 7.8}]),
                    "9": (TEXT_FORMAT, 'Hidden Figures'),
                    "10": (TEXT_FORMAT_UNORDERED_LIST, ['Taraji P. Henson', 'Octavia Spencer', 'Janelle Monáe']),
                    "11": (TEXT_FORMAT_UNORDERED_LIST, ['Theodore Melfi']),
                    "12": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Aliens in the Attic',
                                                          'year': 2009,
                                                          'duration': 86,
                                                          'genres': ['Adventure', 'Comedy', 'Family'],
                                                          'rating': 5.4,
                                                          'directors': ['John Schultz'],
                                                          'cast': ['Ashley Tisdale',
                                                           'Robert Hoffman',
                                                           'Carter Jenkins',
                                                           'Austin Butler']},
                                                         {'title': 'Dark Buenos Aires',
                                                          'year': 2010,
                                                          'duration': 90,
                                                          'genres': ['Thriller'],
                                                          'rating': 4.8,
                                                          'directors': ['Ramon Térmens'],
                                                          'cast': ['Francesc Garrido',
                                                           'Daniel Faraldo',
                                                           'Natasha Yarovenko',
                                                           'Julieta Díaz']},
                                                         {'title': 'The Bank Shot',
                                                          'year': 1974,
                                                          'duration': 83,
                                                          'genres': ['Comedy', 'Crime'],
                                                          'rating': 5.4,
                                                          'directors': ['Gower Champion'],
                                                          'cast': ['George C. Scott', 'Joanna Cassidy', 'Sorrell Booke', 'G. Wood']},
                                                         {'title': 'Complicity',
                                                          'year': 2013,
                                                          'duration': 81,
                                                          'genres': ['Drama', 'Thriller'],
                                                          'rating': 4.1,
                                                          'directors': ['C.B. Harding'],
                                                          'cast': ['Sean Young', 'Jenna Boyd', 'Heather Hemmens', 'Haley Ramm']},
                                                         {'title': "Russia's Toughest Prisons",
                                                          'year': 2011,
                                                          'duration': 60,
                                                          'genres': ['Documentary'],
                                                          'rating': 6.5,
                                                          'directors': ['Anna Rodzinski'],
                                                          'cast': ['Alexander Brandon']},
                                                         {'title': 'Broken Soldier',
                                                          'year': 2022,
                                                          'duration': 93,
                                                          'genres': ['Drama', 'Thriller'],
                                                          'rating': 3.4,
                                                          'directors': ['Matthew Coppola'],
                                                          'cast': ['Mark Kassen', 'Sophie Turner', 'Ray Liotta', 'Ivana Milicevic']},
                                                         {'title': 'Dear John',
                                                          'year': 1988,
                                                          'duration': 108,
                                                          'genres': ['Horror', 'Thriller'],
                                                          'rating': 4.4,
                                                          'directors': ['Catherine Ord'],
                                                          'cast': ['William Bledsoe',
                                                           'Valerie Buhagiar',
                                                           'Stan Lake',
                                                           'Thomas Rickert',
                                                           'Daniel MacIvor',
                                                           'David Maclean',
                                                           'Evelyn Kaye']},
                                                         {'title': 'Strange Cargo',
                                                          'year': 1936,
                                                          'duration': 68,
                                                          'genres': ['Crime', 'Drama'],
                                                          'rating': 7.2,
                                                          'directors': ['Lawrence Huntington'],
                                                          'cast': ['Kenneth Warrington',
                                                           'Kathleen Kelly',
                                                           'George Mozart',
                                                           'Moore Marriott',
                                                           'George Sanders',
                                                           'Richard Norris',
                                                           'Geoffrey Clarke']},
                                                         {'title': 'The Man from Colorado',
                                                          'year': 1948,
                                                          'duration': 100,
                                                          'genres': ['Romance', 'Western'],
                                                          'rating': 6.6,
                                                          'directors': ['Henry Levin'],
                                                          'cast': ['Glenn Ford', 'William Holden', 'Ellen Drew', 'Ray Collins']},
                                                         {'title': 'The Wild Ones',
                                                          'year': 2012,
                                                          'duration': 100,
                                                          'genres': ['Drama'],
                                                          'rating': 6.2,
                                                          'directors': ['Patricia Ferreira'],
                                                          'cast': ['Marina Comas', 'Àlex Monner', 'Albert Baró', 'Aina Clotet']},
                                                         {'title': 'Panama Sugar',
                                                          'year': 1990,
                                                          'duration': 110,
                                                          'genres': ['Comedy'],
                                                          'rating': 4.4,
                                                          'directors': ['Marcello Avallone'],
                                                          'cast': ['Scott Plank',
                                                           'Oliver Reed',
                                                           'Lucrezia Lante della Rovere',
                                                           'Vittorio Amandola']},
                                                         {'title': 'Maa Beti',
                                                          'year': 1986,
                                                          'duration': 151,
                                                          'genres': ['Drama'],
                                                          'rating': 5.5,
                                                          'directors': ['Kalpataru'],
                                                          'cast': ['Shashi Kapoor',
                                                           'Meenakshi Sheshadri',
                                                           'Sharmila Tagore',
                                                           'Tanuja Samarth']},
                                                         {'title': 'Rites of Passage',
                                                          'year': 2013,
                                                          'duration': 80,
                                                          'genres': ['Drama'],
                                                          'rating': 6.6,
                                                          'directors': ['Phillip Crawford', 'Mary Callaghan', 'Gemma Parsons'],
                                                          'cast': ['Chaise Barbaric', 'Skie Carlson', 'Tiran Dingle', 'Elias Rees']},
                                                         {'title': 'All in',
                                                          'year': 2005,
                                                          'duration': 95,
                                                          'genres': ['Comedy'],
                                                          'rating': 7.0,
                                                          'directors': ['Reggie Jordan'],
                                                          'cast': ['Edward Asner', 'Ahmed Ahmed', 'Jim Formanek', 'Matt Godecker']},
                                                         {'title': 'The State of Texas vs. Melissa',
                                                          'year': 2020,
                                                          'duration': 102,
                                                          'genres': ['Documentary'],
                                                          'rating': 5.8,
                                                          'directors': ['Cyril Thomas', 'Sabrina Van Tassel'],
                                                          'cast': ['Norma Jean Farley',
                                                           'Peter Gilman',
                                                           'Bobby Lucio',
                                                           'Daniella Lucio']},
                                                         {'title': 'Bad Day',
                                                          'year': 2008,
                                                          'duration': 98,
                                                          'genres': ['Crime', 'Thriller'],
                                                          'rating': 4.1,
                                                          'directors': ['Ian David Diaz'],
                                                          'cast': ['Claire Goose', 'Donna Air', 'Anthony Ofoegbu', 'George Calil']},
                                                         {'title': 'The Stonecutter',
                                                          'year': 2000,
                                                          'duration': 95,
                                                          'genres': ['Drama'],
                                                          'rating': 8.3,
                                                          'directors': ['Stephen Erickson'],
                                                          'cast': ['Michael Cavalieri',
                                                           'Trisha Melynkov',
                                                           'Harold Cannon',
                                                           'Karin Argoud']},
                                                         {'title': "Thunder in God's Country",
                                                          'year': 1951,
                                                          'duration': 67,
                                                          'genres': ['Western'],
                                                          'rating': 6.9,
                                                          'directors': ['George Blair'],
                                                          'cast': ['Paul Harvey',
                                                           'Rex Allen',
                                                           'Mary Ellen Kay',
                                                           'Buddy Ebsen',
                                                           'Ian MacDonald']},
                                                         {'title': 'When Elephants Fight',
                                                          'year': 2015,
                                                          'duration': 90,
                                                          'genres': ['Documentary', 'News'],
                                                          'rating': 7.7,
                                                          'directors': ['Mike Ramsdell'],
                                                          'cast': ['Robin Wright']},
                                                         {'title': 'To Gillian on Her 37th Birthday',
                                                          'year': 1996,
                                                          'duration': 93,
                                                          'genres': ['Drama', 'Fantasy', 'Romance'],
                                                          'rating': 5.8,
                                                          'directors': ['Michael Pressman'],
                                                          'cast': ['Peter Gallagher',
                                                           'Michelle Pfeiffer',
                                                           'Claire Danes',
                                                           'Laurie Fortier']}]),
                    "13": (TEXT_FORMAT, 4262),
                    "14": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Little Women',
                                                          'year': 1933,
                                                          'duration': 115,
                                                          'genres': ['Drama', 'Family', 'Romance'],
                                                          'rating': 7.2,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Joan Bennett',
                                                           'Paul Lukas',
                                                           'Edna May Oliver']},
                                                         {'title': 'Desk Set',
                                                          'year': 1957,
                                                          'duration': 103,
                                                          'genres': ['Comedy', 'Romance'],
                                                          'rating': 7.2,
                                                          'directors': ['Walter Lang'],
                                                          'cast': ['Spencer Tracy',
                                                           'Katharine Hepburn',
                                                           'Gig Young',
                                                           'Joan Blondell']},
                                                         {'title': 'Woman of the Year',
                                                          'year': 1942,
                                                          'duration': 114,
                                                          'genres': ['Comedy', 'Drama', 'Romance'],
                                                          'rating': 7.2,
                                                          'directors': ['George Stevens'],
                                                          'cast': ['Spencer Tracy',
                                                           'Katharine Hepburn',
                                                           'Fay Bainter',
                                                           'Reginald Owen']},
                                                         {'title': 'Quality Street',
                                                          'year': 1937,
                                                          'duration': 83,
                                                          'genres': ['Comedy', 'Drama', 'Romance'],
                                                          'rating': 6.2,
                                                          'directors': ['George Stevens'],
                                                          'cast': ['Katharine Hepburn', 'Franchot Tone', 'Eric Blore', 'Fay Bainter']},
                                                         {'title': 'Love Affair',
                                                          'year': 1994,
                                                          'duration': 108,
                                                          'genres': ['Comedy', 'Drama', 'Romance'],
                                                          'rating': 6.0,
                                                          'directors': ['Glenn Gordon Caron'],
                                                          'cast': ['Warren Beatty',
                                                           'Annette Bening',
                                                           'Katharine Hepburn',
                                                           'Garry Shandling']},
                                                         {'title': "Guess Who's Coming to Dinner",
                                                          'year': 1967,
                                                          'duration': 108,
                                                          'genres': ['Comedy', 'Drama'],
                                                          'rating': 7.8,
                                                          'directors': ['Stanley Kramer'],
                                                          'cast': ['Spencer Tracy',
                                                           'Sidney Poitier',
                                                           'Katharine Hepburn',
                                                           'Katharine Houghton']},
                                                         {'title': 'Dragon Seed',
                                                          'year': 1944,
                                                          'duration': 148,
                                                          'genres': ['Drama', 'History', 'War'],
                                                          'rating': 6.0,
                                                          'directors': ['Harold S. Bucquet', 'Jack Conway'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Walter Huston',
                                                           'Aline MacMahon',
                                                           'Akim Tamiroff']},
                                                         {'title': 'The Trojan Women',
                                                          'year': 1971,
                                                          'duration': 105,
                                                          'genres': ['Drama'],
                                                          'rating': 6.8,
                                                          'directors': ['Michael Cacoyannis'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Vanessa Redgrave',
                                                           'Geneviève Bujold',
                                                           'Irene Papas']},
                                                         {'title': 'The Madwoman of Chaillot',
                                                          'year': 1969,
                                                          'duration': 132,
                                                          'genres': ['Comedy', 'Drama'],
                                                          'rating': 6.0,
                                                          'directors': ['Bryan Forbes'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Paul Henreid',
                                                           'Oskar Homolka',
                                                           'Yul Brynner']},
                                                         {'title': 'Without Love',
                                                          'year': 1945,
                                                          'duration': 111,
                                                          'genres': ['Comedy', 'Romance'],
                                                          'rating': 6.6,
                                                          'directors': ['Harold S. Bucquet'],
                                                          'cast': ['Spencer Tracy',
                                                           'Katharine Hepburn',
                                                           'Lucille Ball',
                                                           'Keenan Wynn']},
                                                         {'title': 'The Philadelphia Story',
                                                          'year': 1940,
                                                          'duration': 112,
                                                          'genres': ['Comedy', 'Romance'],
                                                          'rating': 7.9,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['Cary Grant', 'Katharine Hepburn', 'James Stewart', 'Ruth Hussey']},
                                                         {'title': 'Pat and Mike',
                                                          'year': 1952,
                                                          'duration': 95,
                                                          'genres': ['Comedy', 'Romance', 'Sport'],
                                                          'rating': 6.9,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['Spencer Tracy', 'Katharine Hepburn', 'Aldo Ray', 'William Ching']},
                                                         {'title': 'The Little Minister',
                                                          'year': 1934,
                                                          'duration': 110,
                                                          'genres': ['Drama', 'Romance'],
                                                          'rating': 6.2,
                                                          'directors': ['Richard Wallace'],
                                                          'cast': ['Katharine Hepburn', 'John Beal', 'Alan Hale', 'Donald Crisp']},
                                                         {'title': 'A Bill of Divorcement',
                                                          'year': 1932,
                                                          'duration': 70,
                                                          'genres': ['Drama'],
                                                          'rating': 6.5,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['John Barrymore',
                                                           'Katharine Hepburn',
                                                           'Billie Burke',
                                                           'David Manners']},
                                                         {'title': 'State of the Union',
                                                          'year': 1948,
                                                          'duration': 124,
                                                          'genres': ['Comedy', 'Drama'],
                                                          'rating': 7.2,
                                                          'directors': ['Frank Capra'],
                                                          'cast': ['Spencer Tracy',
                                                           'Katharine Hepburn',
                                                           'Van Johnson',
                                                           'Angela Lansbury']},
                                                         {'title': 'The Sea of Grass',
                                                          'year': 1947,
                                                          'duration': 123,
                                                          'genres': ['Drama', 'Western'],
                                                          'rating': 6.3,
                                                          'directors': ['Elia Kazan'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Spencer Tracy',
                                                           'Robert Walker',
                                                           'Melvyn Douglas']},
                                                         {'title': 'Spitfire',
                                                          'year': 1934,
                                                          'duration': 87,
                                                          'genres': ['Drama'],
                                                          'rating': 5.4,
                                                          'directors': ['John Cromwell'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Robert Young',
                                                           'Ralph Bellamy',
                                                           'Martha Sleeper']},
                                                         {'title': 'Bringing Up Baby',
                                                          'year': 1938,
                                                          'duration': 102,
                                                          'genres': ['Comedy'],
                                                          'rating': 7.8,
                                                          'directors': ['Howard Hawks'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Cary Grant',
                                                           'Charles Ruggles',
                                                           'Walter Catlett']},
                                                         {'title': 'A Delicate Balance',
                                                          'year': 1973,
                                                          'duration': 133,
                                                          'genres': ['Drama'],
                                                          'rating': 6.6,
                                                          'directors': ['Tony Richardson'],
                                                          'cast': ['Katharine Hepburn', 'Paul Scofield', 'Lee Remick', 'Kate Reid']},
                                                         {'title': 'Olly, Olly, Oxen Free',
                                                          'year': 1978,
                                                          'duration': 89,
                                                          'genres': ['Adventure'],
                                                          'rating': 5.3,
                                                          'directors': ['Richard A. Colla'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Kevin McKenzie',
                                                           'Dennis Dimster',
                                                           'Peter Kilman']},
                                                         {'title': 'Keeper of the Flame',
                                                          'year': 1942,
                                                          'duration': 100,
                                                          'genres': ['Drama', 'Mystery'],
                                                          'rating': 6.7,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['Spencer Tracy',
                                                           'Katharine Hepburn',
                                                           'Richard Whorf',
                                                           'Margaret Wycherly']},
                                                         {'title': 'Christopher Strong',
                                                          'year': 1933,
                                                          'duration': 78,
                                                          'genres': ['Action', 'Adventure', 'Drama'],
                                                          'rating': 6.3,
                                                          'directors': ['Dorothy Arzner'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Colin Clive',
                                                           'Billie Burke',
                                                           'Helen Chandler']},
                                                         {'title': 'The Rainmaker',
                                                          'year': 1956,
                                                          'duration': 121,
                                                          'genres': ['Romance', 'Western'],
                                                          'rating': 6.9,
                                                          'directors': ['Joseph Anthony'],
                                                          'cast': ['Burt Lancaster',
                                                           'Katharine Hepburn',
                                                           'Wendell Corey',
                                                           'Lloyd Bridges']},
                                                         {'title': 'Summertime',
                                                          'year': 1955,
                                                          'duration': 102,
                                                          'genres': ['Comedy', 'Drama', 'Romance'],
                                                          'rating': 7.1,
                                                          'directors': ['David Lean'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Rossano Brazzi',
                                                           'Isa Miranda',
                                                           'Darren McGavin']},
                                                         {'title': 'On Golden Pond',
                                                          'year': 1981,
                                                          'duration': 109,
                                                          'genres': ['Drama'],
                                                          'rating': 7.6,
                                                          'directors': ['Mark Rydell'],
                                                          'cast': ['Katharine Hepburn', 'Henry Fonda', 'Jane Fonda', 'Doug McKeon']},
                                                         {'title': 'Suddenly, Last Summer',
                                                          'year': 1959,
                                                          'duration': 114,
                                                          'genres': ['Drama', 'Mystery', 'Thriller'],
                                                          'rating': 7.5,
                                                          'directors': ['Joseph L. Mankiewicz'],
                                                          'cast': ['Elizabeth Taylor',
                                                           'Katharine Hepburn',
                                                           'Montgomery Clift',
                                                           'Albert Dekker']},
                                                         {'title': 'Mary of Scotland',
                                                          'year': 1936,
                                                          'duration': 123,
                                                          'genres': ['Biography', 'Drama', 'History'],
                                                          'rating': 6.3,
                                                          'directors': ['John Ford', 'Leslie Goodwins'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Fredric March',
                                                           'Florence Eldridge',
                                                           'Douglas Walton']},
                                                         {'title': 'Morning Glory',
                                                          'year': 1933,
                                                          'duration': 74,
                                                          'genres': ['Drama', 'Romance'],
                                                          'rating': 6.4,
                                                          'directors': ['Lowell Sherman'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Douglas Fairbanks Jr.',
                                                           'Adolphe Menjou',
                                                           'Mary Duncan']},
                                                         {'title': 'The Lion in Winter',
                                                          'year': 1968,
                                                          'duration': 134,
                                                          'genres': ['Biography', 'Drama', 'History'],
                                                          'rating': 7.9,
                                                          'directors': ['Anthony Harvey'],
                                                          'cast': ["Peter O'Toole",
                                                           'Katharine Hepburn',
                                                           'Anthony Hopkins',
                                                           'John Castle']},
                                                         {'title': 'Break of Hearts',
                                                          'year': 1935,
                                                          'duration': 78,
                                                          'genres': ['Drama', 'Romance'],
                                                          'rating': 5.8,
                                                          'directors': ['Philip Moeller'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Charles Boyer',
                                                           'John Beal',
                                                           'Jean Hersholt']},
                                                         {'title': 'The Iron Petticoat',
                                                          'year': 1956,
                                                          'duration': 87,
                                                          'genres': ['Comedy'],
                                                          'rating': 5.1,
                                                          'directors': ['Ralph Thomas'],
                                                          'cast': ['Bob Hope',
                                                           'Katharine Hepburn',
                                                           'Noelle Middleton',
                                                           'James Robertson Justice']},
                                                         {'title': 'Stage Door',
                                                          'year': 1937,
                                                          'duration': 92,
                                                          'genres': ['Comedy', 'Drama'],
                                                          'rating': 7.7,
                                                          'directors': ['Gregory La Cava'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Ginger Rogers',
                                                           'Adolphe Menjou',
                                                           'Gail Patrick']},
                                                         {'title': 'Rooster Cogburn',
                                                          'year': 1975,
                                                          'duration': 108,
                                                          'genres': ['Adventure', 'Drama', 'Western'],
                                                          'rating': 6.8,
                                                          'directors': ['Stuart Millar'],
                                                          'cast': ['John Wayne',
                                                           'Katharine Hepburn',
                                                           'Anthony Zerbe',
                                                           'Richard Jordan']},
                                                         {'title': "Long Day's Journey Into Night",
                                                          'year': 1962,
                                                          'duration': 174,
                                                          'genres': ['Drama'],
                                                          'rating': 7.5,
                                                          'directors': ['Sidney Lumet'],
                                                          'cast': ['Katharine Hepburn',
                                                           'Ralph Richardson',
                                                           'Jason Robards',
                                                           'Dean Stockwell']},
                                                         {'title': 'Sylvia Scarlett',
                                                          'year': 1935,
                                                          'duration': 95,
                                                          'genres': ['Comedy', 'Drama', 'Romance'],
                                                          'rating': 6.2,
                                                          'directors': ['George Cukor'],
                                                          'cast': ['Katharine Hepburn', 'Cary Grant', 'Brian Aherne', 'Edmund Gwenn']}]),
                    "15": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Wisconsin Death Trip',
                                                          'year': 1999,
                                                          'duration': 76,
                                                          'genres': ['Biography', 'Crime', 'Drama'],
                                                          'rating': 6.6,
                                                          'directors': ['James Marsh'],
                                                          'cast': ['Ian Holm', 'Jeffrey Golden', 'Jo Vukelich', 'Marcus Monroe']},
                                                         {'title': 'Bootleg Wisconsin',
                                                          'year': 2008,
                                                          'duration': 73,
                                                          'genres': ['Drama'],
                                                          'rating': 7.7,
                                                          'directors': ['Brandon Linden'],
                                                          'cast': ['Lepolion Henderson',
                                                           'Angela Harris',
                                                           'Alissa Bailey',
                                                           'Joyce Porter']},
                                                         {'title': 'Wisconsin Supper Clubs: An Old Fashioned Experience',
                                                          'year': 2011,
                                                          'duration': 55,
                                                          'genres': ['Documentary', 'History'],
                                                          'rating': 6.7,
                                                          'directors': ['Ron Faiola'],
                                                          'cast': ['Bun E. Carlos']},
                                                         {'title': 'Small Town Wisconsin',
                                                          'year': 2020,
                                                          'duration': 109,
                                                          'genres': ['Comedy', 'Drama'],
                                                          'rating': 7.3,
                                                          'directors': ['Niels Mueller'],
                                                          'cast': ['David Sullivan',
                                                           'Bill Heck',
                                                           'Kristen Johnston',
                                                           'Cooper J. Friedman']}]),
                    "16": (TEXT_FORMAT, 26),
                    "17": (TEXT_FORMAT, 153),
                    "18": (TEXT_FORMAT_ORDERED_LIST, ['American Barbarian',
                                                         'The Children Under the House',
                                                         'Santhoshathil Kalavaram',
                                                         'La Bruja',
                                                         'Laurence',
                                                         'Muttnik',
                                                         'Cold Calm',
                                                         'Heavy Makeup',
                                                         'Girls on a Boat',
                                                         'Phantom Summer']),
                    "19": (TEXT_FORMAT, 'Comedy'),
                    "20": (TEXT_FORMAT_UNORDERED_LIST, ['Michael Kirk',
                                                         'A.J. Martinson',
                                                         'Anthony Moffat',
                                                         'Jason Harney',
                                                         'Thomas A. Morgan'])}

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
        else:
            if expected != actual:
                return "expected %s but found %s " % (repr(expected), repr(actual))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def simple_compare(expected, actual, complete_msg=True):
    msg = PASS
    if type(expected) == type:
        if expected != actual:
            if type(actual) == type:
                msg = "expected %s but found %s" % (expected.__name__, actual.__name__)
            else:
                msg = "expected %s but found %s" % (expected.__name__, repr(actual))
    elif type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg

def namedtuple_compare(expected, actual):
    msg = PASS
    for field in expected._fields:
        val = simple_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (field, type(expected).__name__) + val
            return msg
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        elif type(expected[i]).__name__ == obfuscate1():
            val = simple_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (list may not be ordered as required)"
            except:
                pass
    return msg


def list_compare_helper(larger, smaller):
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], False)
                break
            val = simple_compare(larger[i], smaller[j], False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg


def list_compare_unordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in %s; expected entries of type %s" % (obj, obj, type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg

def list_compare_special_init(expected, special_order):
    real_expected = []
    for i in range(len(expected)):
        if real_expected == [] or special_order[i-1] != special_order[i]:
            real_expected.append([])
        real_expected[-1].append(expected[i])
    return real_expected


def list_compare_special(expected, actual, special_order):
    expected = list_compare_special_init(expected, special_order)
    msg = PASS
    expected_list = []
    for expected_item in expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in expected:
            j = len(expected_item)
            actual_item = actual[i: i + j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i + j - 1) + val
                msg = msg + " (list may not be ordered as required)"
                break
            i += j

    return msg


def dict_compare(expected, actual, obj="dict"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
    except:
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (
            type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if expected[key] == None or type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub" + obj)
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg


def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)

def check_file_size(path):
    size = os.path.getsize(path)
    assert size < MAX_FILE_SIZE * 10**3, "Your file is too big to be processed by Gradescope; please delete unnecessary output cells so your file size is < %s KB" % MAX_FILE_SIZE
