import string

class EditDist:
    def elimination_dist(self,ori_str,dst_str):
        ori_str=ori_str.strip().rstrip()
        dst_str=dst_str.strip().rstrip()
        len1=len(ori_str)
        len2=len(dst_str)
        if len1==0 or len2==0:
            return max(len1,len2)*2
        sub_dst_str=dst_str
        sub_ori_str=ori_str
        for end_pos in range(len2,0,-1):
            find_pos=sub_ori_str.find(sub_dst_str[0:end_pos])
            if find_pos==-1:
                continue
            new_sub=""
            if find_pos>0:
                new_sub=sub_ori_str[0:find_pos]
            if find_pos+end_pos<len1:
                new_sub+=sub_ori_str[find_pos+end_pos:]
            sub_ori_str=new_sub
            sub_dst_str=dst_str[end_pos:]
            break
        sub_len=len(sub_dst_str)
        for start_pos in range(0,sub_len):
            find_pos=sub_ori_str.find(sub_dst_str[start_pos:])
            if find_pos==-1:
                continue
            new_sub=""
            if find_pos>0:
                new_sub=sub_ori_str[0:find_pos]
            if find_pos+len(sub_dst_str[start_pos:])<len(sub_ori_str):
                new_sub+=sub_ori_str[find_pos+len(sub_dst_str[start_pos:]):]
            sub_ori_str=new_sub
            break
        return len(sub_ori_str)+len(sub_dst_str)
            
        
    def cal_edit_dist(self,str1,str2):
        if len(str1)==0 or len(str2)==0:
            return max(len(str1),len(str2))
        init=0
        if str1[0]!=str2[0]:
            init=1
        dist=[]
        for i in range(0,len(str1)):
            for j in range(0,len(str2)):
                if j==0 and i==0:
                    dist2=[]
                    dist2.append(init)
                    dist.append(dist2)
                    continue
                if j==0:
                    dist2=[]
                    dist2.append(100000)
                    dist.append(dist2)
                else:
                    dist[i].append(100000)
        cost=0
        for i in range(0,len(str1)):
            for j in range(0,len(str2)):
                if j==0 and i==0:
                    continue
                if str1[i]==str2[j]:
                    cost=0
                else:
                    cost=1
                if i>0 and j>0:
                    dist[i][j]=min(dist[i-1][j]+1,dist[i][j-1]+1,dist[i-1][j-1]+cost)
                elif i==1 or j==1:
                    dist[i][j]=max(cost+init,1)
        last_dist=dist[len(str1)-1][len(str2)-1]
        return last_dist
           

    
