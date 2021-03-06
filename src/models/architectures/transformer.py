import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import ipdb

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        
        self.register_buffer('pe', pe)

    def forward(self, x):
        # not used in the final model
        x = x + self.pe[:x.shape[0], :]
        return self.dropout(x)


# only for ablation / not used in the final model
class TimeEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(TimeEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x, mask, lengths):
        time = mask * 1/(lengths[..., None]-1)
        time = time[:, None] * torch.arange(time.shape[1], device=x.device)[None, :]
        time = time[:, 0].T
        # add the time encoding
        x = x + time[..., None]
        return self.dropout(x)
    

class Encoder_TRANSFORMER(nn.Module):
    def __init__(self, modeltype, njoints, nfeats, num_frames, num_classes, translation, pose_rep, glob, glob_rot, compositional_actions,
                 latent_dim=256, ff_size=1024, num_layers=4, num_heads=4, dropout=0.1,
                 ablation=None, activation="gelu", **kargs):
        super().__init__()
        
        self.modeltype = modeltype
        self.njoints = njoints
        self.nfeats = nfeats
        self.num_frames = num_frames
        self.num_classes = num_classes
        
        self.pose_rep = pose_rep
        self.glob = glob
        self.glob_rot = glob_rot
        self.translation = translation
        
        self.latent_dim = latent_dim
        
        self.ff_size = ff_size
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.dropout = dropout

        self.ablation = ablation
        self.activation = activation
        
        self.input_feats = self.njoints*self.nfeats
        self.compositional_actions = compositional_actions
        self.num_classes = 10+25
        if self.ablation == "average_encoder":
            self.mu_layer = nn.Linear(self.latent_dim, self.latent_dim)
            self.sigma_layer = nn.Linear(self.latent_dim, self.latent_dim)
        else:
          #  self.muQuery = nn.Parameter(torch.randn(self.num_classes, self.latent_dim))
          #  self.sigmaQuery = nn.Parameter(torch.randn(self.num_classes, self.latent_dim))
            self.muQuery = nn.Parameter(torch.randn(10+25, self.latent_dim))
            self.sigmaQuery = nn.Parameter(torch.randn(10+25, self.latent_dim))
        
        self.skelEmbedding = nn.Linear(self.input_feats, self.latent_dim)
        
        self.sequence_pos_encoder = PositionalEncoding(self.latent_dim, self.dropout)
        
        # self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        
        seqTransEncoderLayer = nn.TransformerEncoderLayer(d_model=self.latent_dim,
                                                          nhead=self.num_heads,
                                                          dim_feedforward=self.ff_size,
                                                          dropout=self.dropout,
                                                          activation=self.activation)
        self.seqTransEncoder = nn.TransformerEncoder(seqTransEncoderLayer,
                                                     num_layers=self.num_layers)

        self.mulinear = nn.Linear(self.num_classes-25, self.latent_dim)
        self.sigmalinear = nn.Linear(self.num_classes-25, self.latent_dim)

    def forward(self, batch):
#        ipdb.set_trace()
        x, y, mask, alphas = batch["x"], batch["y"], batch["mask"], batch["alpha"]
       # x, y1, y2, mask, alphas = batch["x"], batch["y1"], batch["y2"], batch["mask"], batch["alphas"]
        bs, njoints, nfeats, nframes = x.shape
        x = x.permute((3, 0, 1, 2)).reshape(nframes, bs, njoints*nfeats)
#        print("x device", x.device)
#        print("self.skelEmbedding", self.skelEmbedding.weight.device)        
        # embedding of the skeleton
        x = self.skelEmbedding(x)
        y_onehot1 = torch.nn.functional.one_hot(torch.tensor(1), num_classes=self.num_classes-25)
        y_onehot4 = torch.nn.functional.one_hot(torch.tensor(4), num_classes=self.num_classes-25)
        y_onehot2 = torch.nn.functional.one_hot(torch.tensor(2), num_classes=self.num_classes-25)
        y_onehot3 = torch.nn.functional.one_hot(torch.tensor(3), num_classes=self.num_classes-25)
        y_onehot5 = torch.nn.functional.one_hot(torch.tensor(5), num_classes=self.num_classes-25)
        y_onehot6 = torch.nn.functional.one_hot(torch.tensor(6), num_classes=self.num_classes-25)
        y_onehot7 = torch.nn.functional.one_hot(torch.tensor(7), num_classes=self.num_classes-25)
        y_onehot9 = torch.nn.functional.one_hot(torch.tensor(9), num_classes=self.num_classes-25)
#        y_onehot11 = torch.nn.functional.one_hot(torch.tensor(11), num_classes=self.num_classes-25)
        y_onehot8 = torch.nn.functional.one_hot(torch.tensor(8), num_classes=self.num_classes-25)
        y_onehot0 = torch.nn.functional.one_hot(torch.tensor(0), num_classes=self.num_classes-25)
#        y_onehot10 = torch.nn.functional.one_hot(torch.tensor(10), num_classes=self.num_classes-25)

        y_onehot1 = y_onehot1.to(x.device)
        y_onehot4 = y_onehot4.to(x.device)
        y_onehot2 = y_onehot2.to(x.device)
        y_onehot3 = y_onehot3.to(x.device)
        y_onehot5 = y_onehot5.to(x.device)
        y_onehot6 = y_onehot6.to(x.device)
        y_onehot7 = y_onehot7.to(x.device)
        y_onehot9 = y_onehot9.to(x.device)
#        y_onehot11 = y_onehot11.to(x.device)
        y_onehot8 = y_onehot8.to(x.device)
        y_onehot0 = y_onehot0.to(x.device)
#        y_onehot10 = y_onehot10.to(x.device)
        
        onehot_all = {0:y_onehot0, 1:y_onehot1, 2:y_onehot2, 3:y_onehot3, 4:y_onehot4, 5:y_onehot5, 6:y_onehot6, 7:y_onehot7,
                      8:y_onehot8, 9:y_onehot9,}
        onehot_all = [ onehot_all[i] for i in range(len(onehot_all)) ]
        onehot_all = torch.stack(onehot_all)

        y_one_hot = torch.nn.functional.one_hot(y, num_classes=self.num_classes)
        y_one_hot = y_one_hot[:, 0:self.num_classes-25]
        y_one_hot = y_one_hot.float()
        alphas = alphas.float()
       
        newclass = torch.where(y>9)
        if len(newclass[0]>0):
            act_class = y[newclass] - 10
            compositional_actions = torch.tensor(self.compositional_actions)
            action_comb = compositional_actions[act_class]
            act1 = action_comb[:,0]
            act2 = action_comb[:,1]
            y_onehot_act1 = onehot_all[act1]
            y_onehot_act2 = onehot_all[act2]
            alpha_y_onehot_act1 = y_onehot_act1 * alphas[newclass].unsqueeze(1).repeat(1,10)
            alpha_y_onehot_act2 = y_onehot_act2 * (1-alphas[newclass]).unsqueeze(1).repeat(1,10)
            y_one_hot[newclass] = alpha_y_onehot_act1 + alpha_y_onehot_act2        

#        for i in range( len(self.compositional_actions) ):
#            act_class = i + 12
#            newclass = np.argwhere( np.array(y.clone().cpu())[list(range(len(y)))] == act_class ).squeeze(1)
#            if len(newclass)>0:
#                action_comb = self.compositional_actions[i]
#                act1 = action_comb[0]
#                act2 = action_comb[1]
#                y_onehot_act1 = onehot_all[act1].unsqueeze(0)
#                y_onehot_act2 = onehot_all[act2].unsqueeze(0)
#                alpha_y_onehot_act1 = torch.einsum("ij,k->kij", y_onehot_act1, alphas[newclass]).squeeze()
#                alpha_y_onehot_act2 = torch.einsum("ij,k->kij", y_onehot_act2, (1-alphas[newclass])).squeeze()
#                y_one_hot[newclass] = alpha_y_onehot_act1 + alpha_y_onehot_act2

        muquery = self.mulinear(y_one_hot.float())
        sigmaquery = self.sigmalinear(y_one_hot.float())       
        
        # only for ablation / not used in the final model
        if self.ablation == "average_encoder":
            # add positional encoding
            x = self.sequence_pos_encoder(x)
            
            # transformer layers
            final = self.seqTransEncoder(x, src_key_padding_mask=~mask)
            # get the average of the output
            z = final.mean(axis=0)
            
            # extract mu and logvar
            mu = self.mu_layer(z)
            logvar = self.sigma_layer(z)
        else:
            # adding the mu and sigma queries
          #  alphas = alphas.unsqueeze(1)
          #  alphas = alphas.repeat(1, self.latent_dim)
          #  mix_muquery = alphas*self.muQuery[y1] + (1-alphas)*self.muQuery[y2]
          #  mix_sigmaquery = alphas*self.sigmaQuery[y1] + (1-alphas)*self.sigmaQuery[y2]
          #  xseq = torch.cat((mix_muquery[None], mix_sigmaquery[None], x), axis=0)
          #  xseq = torch.cat((self.muQuery[y][None], self.sigmaQuery[y][None], x), axis=0)
            xseq = torch.cat((muquery[None], sigmaquery[None], x), axis=0)
            # add positional encoding
            xseq = self.sequence_pos_encoder(xseq)

            # create a bigger mask, to allow attend to mu and sigma
            muandsigmaMask = torch.ones((bs, 2), dtype=bool, device=x.device)
            maskseq = torch.cat((muandsigmaMask, mask), axis=1)

            final = self.seqTransEncoder(xseq, src_key_padding_mask=~maskseq)
            mu = final[0]
            logvar = final[1]
            
        return {"mu": mu, "logvar": logvar}


class Decoder_TRANSFORMER(nn.Module):
    def __init__(self, modeltype, njoints, nfeats, num_frames, num_classes, translation, pose_rep, glob, glob_rot, compositional_actions,
                 latent_dim=256, ff_size=1024, num_layers=4, num_heads=4, dropout=0.1, activation="gelu",
                 ablation=None, **kargs):
        super().__init__()

        self.modeltype = modeltype
        self.njoints = njoints
        self.nfeats = nfeats
        self.num_frames = num_frames
        self.num_classes = num_classes
        
        self.pose_rep = pose_rep
        self.glob = glob
        self.glob_rot = glob_rot
        self.translation = translation
        
        self.latent_dim = latent_dim
        
        self.ff_size = ff_size
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.dropout = dropout

        self.ablation = ablation

        self.activation = activation
                
        self.input_feats = self.njoints*self.nfeats
        self.compositional_actions = compositional_actions
        self.num_classes = 35
        # only for ablation / not used in the final model
        if self.ablation == "zandtime":
            self.ztimelinear = nn.Linear(self.latent_dim + self.num_classes, self.latent_dim)
        else:
        #    self.actionBiases = nn.Parameter(torch.randn(self.num_classes, self.latent_dim))
            self.actionBiases = nn.Parameter(torch.randn(10+25, self.latent_dim))

        # only for ablation / not used in the final model
        if self.ablation == "time_encoding":
            self.sequence_pos_encoder = TimeEncoding(self.dropout)
        else:
            self.sequence_pos_encoder = PositionalEncoding(self.latent_dim, self.dropout)
        
        seqTransDecoderLayer = nn.TransformerDecoderLayer(d_model=self.latent_dim,
                                                          nhead=self.num_heads,
                                                          dim_feedforward=self.ff_size,
                                                          dropout=self.dropout,
                                                          activation=activation)
        self.seqTransDecoder = nn.TransformerDecoder(seqTransDecoderLayer,
                                                     num_layers=self.num_layers)
        
        self.finallayer = nn.Linear(self.latent_dim, self.input_feats)
        self.actionlinear = nn.Linear(self.num_classes-25, self.latent_dim)        

    def forward(self, batch):
#        ipdb.set_trace()
        z, y, mask, lengths, alphas = batch["z"], batch["y"], batch["mask"], batch["lengths"], batch["alpha"]
      #  z, y1, y2, mask, lengths, alphas = batch["z"], batch["y1"], batch["y2"], batch["mask"], batch["lengths"], batch["alphas"]
        latent_dim = z.shape[1]
        bs, nframes = mask.shape
        njoints, nfeats = self.njoints, self.nfeats

        y_onehot1 = torch.nn.functional.one_hot(torch.tensor(1), num_classes=self.num_classes-25)
        y_onehot4 = torch.nn.functional.one_hot(torch.tensor(4), num_classes=self.num_classes-25)
        y_onehot2 = torch.nn.functional.one_hot(torch.tensor(2), num_classes=self.num_classes-25)
        y_onehot3 = torch.nn.functional.one_hot(torch.tensor(3), num_classes=self.num_classes-25)
        y_onehot5 = torch.nn.functional.one_hot(torch.tensor(5), num_classes=self.num_classes-25)
        y_onehot6 = torch.nn.functional.one_hot(torch.tensor(6), num_classes=self.num_classes-25)
        y_onehot7 = torch.nn.functional.one_hot(torch.tensor(7), num_classes=self.num_classes-25)
        y_onehot9 = torch.nn.functional.one_hot(torch.tensor(9), num_classes=self.num_classes-25)
#        y_onehot11 = torch.nn.functional.one_hot(torch.tensor(11), num_classes=self.num_classes-9)
        y_onehot8 = torch.nn.functional.one_hot(torch.tensor(8), num_classes=self.num_classes-25)
        y_onehot0 = torch.nn.functional.one_hot(torch.tensor(0), num_classes=self.num_classes-25)
#        y_onehot10 = torch.nn.functional.one_hot(torch.tensor(10), num_classes=self.num_classes-9)
 
        y_onehot1 = y_onehot1.to(z.device)
        y_onehot4 = y_onehot4.to(z.device)
        y_onehot2 = y_onehot2.to(z.device)
        y_onehot3 = y_onehot3.to(z.device)
        y_onehot5 = y_onehot5.to(z.device)
        y_onehot6 = y_onehot6.to(z.device)
        y_onehot7 = y_onehot7.to(z.device)
        y_onehot9 = y_onehot9.to(z.device)
#        y_onehot11 = y_onehot11.to(z.device)
        y_onehot8 = y_onehot8.to(z.device)
        y_onehot0 = y_onehot0.to(z.device)
#        y_onehot10 = y_onehot10.to(z.device)

        onehot_all = {0:y_onehot0, 1:y_onehot1, 2:y_onehot2, 3:y_onehot3, 4:y_onehot4, 5:y_onehot5, 6:y_onehot6, 7:y_onehot7,
                      8:y_onehot8, 9:y_onehot9 }
 
        onehot_all = [ onehot_all[i] for i in range(len(onehot_all)) ]
        onehot_all = torch.stack(onehot_all)

        y_one_hot = torch.nn.functional.one_hot(y, num_classes=self.num_classes)
        y_one_hot = y_one_hot[:, 0:self.num_classes-25]
        y_one_hot = y_one_hot.float()
        alphas = alphas.float()

        newclass = torch.where(y>9)
        if len(newclass[0]>0):
            act_class = y[newclass] - 10
            compositional_actions = torch.tensor(self.compositional_actions)
            action_comb = compositional_actions[act_class]
            act1 = action_comb[:,0]
            act2 = action_comb[:,1]
            y_onehot_act1 = onehot_all[act1]
            y_onehot_act2 = onehot_all[act2]
            alpha_y_onehot_act1 = y_onehot_act1 * alphas[newclass].unsqueeze(1).repeat(1,10)
            alpha_y_onehot_act2 = y_onehot_act2 * (1-alphas[newclass]).unsqueeze(1).repeat(1,10)
            y_one_hot[newclass] = alpha_y_onehot_act1 + alpha_y_onehot_act2

#        for i in range( len(self.compositional_actions) ):
#            act_class = i + 12
#            newclass = np.argwhere( np.array(y.clone().cpu())[list(range(len(y)))] == act_class ).squeeze(1)
#            if len(newclass)>0:
#                action_comb = self.compositional_actions[i]
#                act1 = action_comb[0]
#                act2 = action_comb[1]
#                y_onehot_act1 = onehot_all[act1].unsqueeze(0)
#                y_onehot_act2 = onehot_all[act2].unsqueeze(0)
#                alpha_y_onehot_act1 = torch.einsum("ij,k->kij", y_onehot_act1, alphas[newclass]).squeeze()
#                alpha_y_onehot_act2 = torch.einsum("ij,k->kij", y_onehot_act2, (1-alphas[newclass])).squeeze()
#                y_one_hot[newclass] = alpha_y_onehot_act1 + alpha_y_onehot_act2

        actiontoken = self.actionlinear(y_one_hot.float())

        # only for ablation / not used in the final model
        if self.ablation == "zandtime":
            yoh = F.one_hot(y, self.num_classes)
            z = torch.cat((z, yoh), axis=1)
            z = self.ztimelinear(z)
            z = z[None]  # sequence of size 1
        else:
            # only for ablation / not used in the final model
            if self.ablation == "concat_bias":
                # sequence of size 2
                z = torch.stack((z, self.actionBiases[y]), axis=0)
            else:
                # shift the latent noise vector to be the action noise
      #          alphas = alphas.unsqueeze(1)
      #          alphas = alphas.repeat(1, latent_dim)
      #          z_action = alphas*self.actionBiases[y1] + (1-alphas)*self.actionBiases[y2]
      #          z = z + z_action
           #     z = z + self.actionBiases[y]
                z = z + actiontoken
                z = z[None]  # sequence of size 1
            
        timequeries = torch.zeros(nframes, bs, latent_dim, device=z.device)
        
        # only for ablation / not used in the final model
        if self.ablation == "time_encoding":
            timequeries = self.sequence_pos_encoder(timequeries, mask, lengths)
        else:
            timequeries = self.sequence_pos_encoder(timequeries)
        
        output = self.seqTransDecoder(tgt=timequeries, memory=z,
                                      tgt_key_padding_mask=~mask)
        
        output = self.finallayer(output).reshape(nframes, bs, njoints, nfeats)
        
        # zero for padded area
        output[~mask.T] = 0
        output = output.permute(1, 2, 3, 0)
        
        batch["output"] = output
        return batch
