from pyssml.AmazonSpeech import AmazonSpeech
from pyssml.PySSML import PySSML

class SSML (AmazonSpeech):
    def prosody(self, attributes, word):
        tag_attributes = ''
        if attributes is None:
            raise TypeError('Parameter attributes must not be None')
        if word is None:
            raise TypeError('Parameter word must not be None')
        try:
            for k, v in attributes.items():
                v = v.lower().strip()
                if v in PySSML.PROSODY_ATTRIBUTES[k]:
                    tag_attributes += " %s='%s'" % (k, v)                
                elif k in ('pitch', 'rate'):
                    rate_value = int(''.join([c for c in v if c in '-0123456789']))
                    tag_attributes += " %s='%d%%'" % (k, rate_value)                    
                elif k == 'volume':
                    rate_value = int(''.join([c for c in v if c in '-0123456789']))
                    tag_attributes += " %s='%ddB'" % (k, rate_value)
                else:
                    raise ValueError('Attribute %s value %s is invalid' % (v, k))
            self.ssml_list.append("<prosody%s>%s</prosody>" % (tag_attributes, self._escape(word)))

        except AttributeError:
            raise AttributeError('Parameters must be strings')
        
        except KeyError:
            raise KeyError('Attribute is unknown')
        
        except ValueError:
            raise ValueError('Attribute value is invalid')
