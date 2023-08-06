# import numpy as np
# import json
import os
class Vocab:
    """
    自动构建vocab词典
    
    """
    def __init__(self):
        #判断文件是否存在
        if os.path.exists('vocab.txt'):
            pass
        else:
            #没有创建
            f = open('vocab.txt','w')
            f.close()
            return {}

    def load_vocab(self):
        """
        加载vocab
        """
        f = open('vocab.txt')
        v={}
        for i,line in enumerate(f):
            # print(line[:-1])
            v[line[:-1]]=i
            # d.update(line[:-1]=i)
        # print(v)
        return v

            
    def add_vocab(self,text_arr):
        """
        添加vocab
        """
        f = open('vocab.txt','a')
        for item in text_arr:
            f.write(item)
            f.write('\n')
        f.close()
        # return
        return True


    def vocab(self,text):
        """
        自动加载
        如果不存在则添加
        """
        vocab=self.load_vocab()
        # print(vocab)
        if text in vocab:
            # print('vocab已经存在')
            return vocab[text]
        else:
            self.add_vocab([text])
            vocab=self.load_vocab()
        return vocab[text]

    def vocab_list(self,word_list):
        """
        处理列表
        """
        vocab_list =[]
        for text in word_list:
            vocab_list.append(self.vocab(text))
        return vocab_list


# # 示例
# word_list=["哈士奇","狗子"]
# vocab=Vocab()
# vocab_list=vocab.vocab_list(word_list)
# print(vocab_list)